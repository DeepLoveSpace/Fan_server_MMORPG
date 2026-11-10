from allauth.account.forms import SignupForm
from django import forms
from .models import User

class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убираем поле username, если оно есть
        if 'username' in self.fields:
            del self.fields['username']

    def save(self, request):
        user = super().save(request)
        # Принудительно ставим email в качестве username, так как AbstractUser его требует
        user.username = user.email 
        user.is_active = False # Блокируем пользователя до ввода кода
        user.save()
        return user

class ConfirmCodeForm(forms.Form):
    code = forms.CharField(max_length=6, label="Код подтверждения из письма")