from django.db import models
from django.conf import settings
from django.urls import reverse

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
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='articles')
    article_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=120)
    text = models.TextField() 
    category = models.ForeignKey(Category, max_length=25, on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return f'Заголовок: {self.title}. Категория: {self.category}'

    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.id)])

class UserResponse(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='responses')
    text = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='responses')
    # Флаг "Принят"
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Отклик от {self.author.email} на {self.article.title}'

class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subscriptions')

    def __str__(self):
        return f'{self.user.email} подписан на {self.category.name}'