from django.conf import settings
from django.db import models
from django.db.models import CASCADE
from django.utils.functional import cached_property

from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=1)
    date = models.DateTimeField(auto_now=True)

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related().all()

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        return sum(map(lambda x: x.quantity, self.get_items_cached))

    @property
    def total_price(self):
        return sum(map(lambda x: x.product_cost, self.get_items_cached))

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk)

    def __str__(self):
        return f'{self.user.username} - {self.product.name} - {self.product.category.name}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
