from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    code = models.CharField(max_length=15, blank=True, null=True)


class Category(models.Model):
    TYPE = (
        ('tank', 'Танки'),
        ('heal', 'Хилы'),
        ('dd', 'ДД'),
        ('buyers', 'Торговцы'),
        ('gildemaster', 'Гилдмастеры'),
        ('quest', 'Квестгиверы'),
        ('smith', 'Кузнецы'),
        ('tanner', 'Кожевники'),
        ('potion', 'Зельевары'),
        ('spellmaster', 'Мастера заклинаний'),
    )
    name = models.CharField(max_length=30, choices=TYPE, unique=True)

    def __str__(self):
        return self.get_name_display()


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    article_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=120)
    text = models.TextField()
    category = models.ForeignKey(Category, max_length=25, on_delete=models.CASCADE)
    upload = models.FileField(upload_to='uploads/')

    def __str__(self):
        return f'Заголовок: {self.title}. Содержание: {self.text}. {self.article_time}. Категория: {self.category}'


    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.id)])

class UserResponse(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.author


class Subscription(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='subscriptions')
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, related_name='subscriptions')

    def __str__(self):
        return self.user
