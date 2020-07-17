from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='media_folder_products')
def media_folder_products(file_name):
    if not file_name:
        file_name = 'products_images/default.jpg'

    return f'{settings.MEDIA_URL}{file_name}'


@register.filter(name='media_folder_users')
def media_folder_users(file_name):
    if not file_name:
        file_name = 'users_avatars/default.jpg'

    return f'{settings.MEDIA_URL}{file_name}'
