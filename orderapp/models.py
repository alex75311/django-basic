from django.contrib.auth import get_user_model
from django.db import models

from mainapp.models import Product


class Order(models.Model):
    FORMING = 'F'
    SENT_TO_PROCEED = 'S'
    PROCEEDED = 'P'
    PAID = 'D'
    READY = 'Y'
    CANCEL = 'C'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'отправлен в обработку'),
        (PAID, 'оплачен'),
        (PROCEEDED, 'обрабатывается'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'отменен'),
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='обновлен', auto_now=True)
    status = models.CharField(verbose_name='статус',
                              max_length=1,
                              choices=ORDER_STATUS_CHOICES,
                              default=FORMING)
    is_active = models.BooleanField(verbose_name='активен', default=True, db_index=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Заказ: {self.id}'

    def get_total_quantity(self):
        items = self.orderitems.all()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_product_type_quantity(self):
        items_count = self.orderitems.all().count()
        return items_count

    def get_total_cost(self):
        items = self.orderitems.all()
        return sum(list(map(lambda x: x.quantity * x.product.price, items)))

    def get_order_product(self):
        items = self.orderitems.all()
        return items

    def delete_quantity_zero(self):
        items = self.orderitems.all()
        return list(map(lambda x: x.quantity == 0, items))

    # переопределяем метод, удаляющий объект
    def delete(self, using=None, keep_parents=False):
        self.is_active = not self.is_active
        if self.status != Order.CANCEL:
            self.status = Order.CANCEL
        else:
            self.status = Order.FORMING
        self.save()

    def order_confirm(self):
        self.status = Order.SENT_TO_PROCEED
        self.save()

    def get_summary(self):
        items = self.orderitems.select_related().all()
        return {
            'total_cost': sum(list(map(lambda x: x.quantity * x.product.price, items))),
            'total_quantity': sum(list(map(lambda x: x.quantity, items))),
        }


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name="orderitems",
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='product',
                                verbose_name='продукт',
                                on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.get(pk=pk)

    def __str__(self):
        return f'{self.product.name} - {self.quantity} шт.'
