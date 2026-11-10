from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import User
import random

@receiver(post_save, sender=User)
def send_confirmation_code(sender, instance, created, **kwargs):
    if created and not instance.is_email_confirmed:
        code = str(random.randint(100000, 999999))
        instance.email_code = code
        instance.save()
        
        send_mail(
            subject='Подтверждение регистрации',
            message=f'Здравствуйте! Ваш код подтверждения: {code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            fail_silently=False,
        )