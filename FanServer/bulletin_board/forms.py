from django import forms
from .models import Article, UserResponse

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'text', 'category']
        widgets = {
            # Подключаем WYSIWYG редактор для поля text
            'text': forms.Textarea(attrs={'class': 'ckeditor'}), 
        }

class ResponseForm(forms.ModelForm):
    class Meta:
        model = UserResponse
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Напишите ваш отклик...'}),
        }