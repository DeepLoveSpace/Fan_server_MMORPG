from django.core.management.base import BaseCommand
from bulletin_board.models import Category

class Command(BaseCommand):
    help = 'Добавляет начальные категории в базу данных'

    def handle(self, *args, **kwargs):
        for code, name in Category.TYPE:
            obj, created = Category.objects.get_or_create(name=code)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Категория "{name}" добавлена'))
            else:
                self.stdout.write(f'Категория "{name}" уже существует')
        self.stdout.write(self.style.SUCCESS('Готово!'))