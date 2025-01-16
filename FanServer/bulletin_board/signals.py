from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from .models import Article, User, UserResponse


@receiver(post_save, sender=Article)
def article_created(instance, created, **kwargs):
    if created:
        subscribers_emails = User.objects.filter(subscriptions__category=instance.category).values_list('email', flat=True)
        subject = f'Новое объявление'
        message = f'Размещено новое объявление в категории {instance.category}. Ссылка на объявление: http://127.0.0.1:8000{instance.get_absolute_url()}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [subscribers_emails]

        send_mail(subject, message, from_email, recipient_list)


@receiver(post_save, sender=UserResponse)
def user_response_created(instance, created, **kwargs):
    if created:
        subject = f'Новый отклик к вашему объявлению'
        message = f'Здравствуйте, {instance.article.author.username}! На Ваше объявление добавлен новый отклик "{instance.article.title}"'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.article.author.email]

        send_mail(subject, message, from_email, recipient_list)
