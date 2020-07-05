from django.db import models


class Category(models.Model):
    name = models.CharField(verbose_name='Категория', max_length=60)
    is_active = models.BooleanField(verbose_name='Активно', default=True)

    def __str__(self):
        return f'id: {self.id} - {self.name}'

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(verbose_name='Название', max_length=60)
    description = models.TextField(verbose_name='Описание', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name='Цена', max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products_images', blank=True)
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=0)
    is_active = models.BooleanField(verbose_name='Активно', default=True)

    def __str__(self):
        return f'{self.name} ({self.category.name})'

    class Meta:
        verbose_name = 'Товары'
        verbose_name_plural = 'Товары'
