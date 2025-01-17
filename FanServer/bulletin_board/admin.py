from django.contrib import admin
from .models import Article, UserResponse, Subscription, Category, User

admin.site.register(Article)
admin.site.register(UserResponse)
admin.site.register(Subscription)
admin.site.register(Category)
admin.site.register(User)