from django.contrib import admin

from authapp.models import ShopUser
from .models import Product, Category

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ShopUser)
