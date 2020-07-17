from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.timezone import now


def get_activation_key_expires():
    return now() + timedelta(hours=48)


class ShopUser(AbstractUser):
    age = models.PositiveIntegerField(verbose_name='Возраст', null=True)
    avatar = models.ImageField(upload_to='users_avatars', verbose_name='Аватар', blank=True)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=get_activation_key_expires)

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    def is_activation_key_expired(self):
        return now() > self.activation_key_expires

    def send_verify_mail(self):
        verify_link = reverse(
            'authapp:verify',
            kwargs={
                'email': self.email,
                'activation_key': self.activation_key,
            },
        )

        title = f'Подтверждение учетной записи {self.username}'
        message = f'Для подтверждения учетной записи {self.username} на портале {settings.DOMAIN_NAME} перейдите по ссылке: ' \
                  f'{settings.DOMAIN_NAME}{verify_link}'

        return send_mail(title, message, settings.EMAIL_HOST_USER, [self.email], fail_silently=False)
