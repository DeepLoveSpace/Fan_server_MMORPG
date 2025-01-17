import datetime
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import mail_managers, EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils import timezone
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from FanServer.bulletin_board.models import Article, Category

logger = logging.getLogger(__name__)


def my_job():
    today = timezone.now()
    last_week = today - datetime.timedelta(days=7)
    articles = Article.objects.filter(article_time__gte=last_week)
    categoriest = set(articles.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(category_name__in=categoriest).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'deily_post.html',
    {
     'link': settings.SITE_URL,
        'articles': articles,
    }
    )

    msg = EmailMultiAlternatives(
        subject='Объявления за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,

    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = 'Runs APScheduler.'

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), 'default')

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second='*/5'), #day_of_week='fri', minute='05', hour='18'
            id='my_job',  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info('Added job "my_job".')

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week='mon', hour='00', minute='00'
            ),
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