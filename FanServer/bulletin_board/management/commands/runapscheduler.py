import datetime
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils import timezone
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

# Правильный импорт моделей
from bulletin_board.models import Article, Category, Subscription

logger = logging.getLogger(__name__)

def my_job():
    today = timezone.now()
    last_week = today - datetime.timedelta(days=7)
    # Берем статьи за последнюю неделю
    articles = Article.objects.filter(article_time__gte=last_week)
    
    if not articles.exists():
        logger.info("Нет новых статей за неделю, рассылка отменена.")
        return

    # Находим категории этих статей
    categories = set(articles.values_list('category__name', flat=True))
    
    # Находим email подписчиков на эти категории
    subscribers = set(Subscription.objects.filter(category__name__in=categories).values_list('user__email', flat=True))

    if not subscribers:
        logger.info("Нет подписчиков для этих категорий.")
        return

    html_content = render_to_string(
        'bulletin_board/newsletter.html',
        {
            'link': settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://127.0.0.1:8000',
            'articles': articles,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Новые объявления за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=list(subscribers),
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    logger.info(f"Рассылка отправлена {len(subscribers)} подписчикам.")

def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

class Command(BaseCommand):
    help = 'Runs APScheduler.'

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), 'default')

        scheduler.add_job(
            my_job,
            # ВНИМАНИЕ: Для теста ставим каждые 5 секунд. Для реальной работы раскомментируй строку с day_of_week
            trigger=CronTrigger(second='*/5'), 
            # trigger=CronTrigger(day_of_week='fri', minute='05', hour='18'),
            id='my_job',
            max_instances=1,
            replace_existing=True,
        )
        logger.info('Added job "my_job".')

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week='mon', hour='00', minute='00'),
            id='delete_old_job_executions',
            max_instances=1,
            replace_existing=True,
        )
        logger.info('Added weekly job: "delete_old_job_executions".')

        try:
            logger.info('Starting scheduler...')
            scheduler.start()
        except KeyboardInterrupt:
            logger.info('Stopping scheduler...')
            scheduler.shutdown()
            logger.info('Scheduler shut down successfully!')