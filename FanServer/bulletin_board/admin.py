from django.contrib import admin
from .models import Article, UserResponse, Subscription, Category

# Регистрируем модели
admin.site.register(Category)
admin.site.register(Article)
admin.site.register(UserResponse)
admin.site.register(Subscription)