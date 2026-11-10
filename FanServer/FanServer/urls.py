from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import confirm_email

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')), # URL-адреса для входа/регистрации от allauth
    path('accounts/confirm/', confirm_email, name='confirm_email'), # Наш код подтверждения
    path('articles/', include('bulletin_board.urls')), # Наши объявления
    path('', include('bulletin_board.urls')), # Чтобы главная открывалась по / (корню)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)