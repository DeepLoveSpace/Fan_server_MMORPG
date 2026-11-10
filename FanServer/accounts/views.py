from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import User
from .forms import ConfirmCodeForm

def confirm_email(request):
    if request.method == 'POST':
        form = ConfirmCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                # Ищем пользователя с таким кодом
                user = User.objects.get(email_code=code, is_email_confirmed=False)
                user.is_email_confirmed = True
                user.is_active = True 
                user.email_code = None 
                user.save()
                
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, "Email успешно подтвержден!")
                return redirect('/') # Перенаправляем на главную (или куда нужно)
            except User.DoesNotExist:
                messages.error(request, "Неверный код или email уже подтвержден.")
    else:
        form = ConfirmCodeForm()
    
    return render(request, 'accounts/confirm_email.html', {'form': form})