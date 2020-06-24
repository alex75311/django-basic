from django.core.management.base import BaseCommand
from authapp.models import ShopUser


class Command(BaseCommand):
    help = 'Создает пользователя django/geekbrains'

    def handle(self, *args, **options):
        if not ShopUser.objects.filter(username='django').exists():
            ShopUser.objects.create_superuser(username='django', password='geekbrains', email='a@a.ru')
