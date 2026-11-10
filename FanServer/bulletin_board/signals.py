from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
# Импортируем правильные модели
from .models import Article, UserResponse 
from accounts.models import User

@receiver(post_save, sender=UserResponse)
def send_reply_notification(sender, instance, created, **kwargs):
    if created:
        # Уведомляем автора объявления о новом отклике
        send_mail(
            subject='Новый отклик на ваше объявление',
            message=f'На ваше объявление "{instance.article.title}" оставлен отклик.\n\nТекст: {instance.text}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.article.author.email],
            fail_silently=True,
        )

@receiver(post_save, sender=UserResponse)
def send_accept_notification(sender, instance, created, **kwargs):
    # Проверяем, не был ли отклик принят только что (если статус изменился на True)
    if not created and instance.status:
        send_mail(
            subject='Ваш отклик принят!',
            message=f'Ваш отклик на объявление "{instance.article.title}" был принят автором.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.author.email],
            fail_silently=True,
        )