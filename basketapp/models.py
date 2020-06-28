from django.conf import settings
from django.db import models
from django.db.models import CASCADE
from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=1)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.product.name} - {self.product.category.name}'

    class Meta:
        verbose_name = 'Корзины'
        verbose_name_plural = 'Корзины'
