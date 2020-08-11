import os
import json

from django.core.management.base import BaseCommand
from mainapp.models import Product, Category
from django.conf import settings


def load_from_json(file_name):
    with open(os.path.join(settings.JSON_PATH, f'{file_name}.json'), 'r', encoding='utf-8') as f:
        return json.load(f)


class Command(BaseCommand):
    help = 'Fill DB new data maipnapp'

    def handle(self, *args, **options):
        categories = load_from_json('categories')

        Category.objects.all().delete()
        [Category.objects.create(**category) for category in categories]

        products = load_from_json('products')
        Product.objects.all().delete()
        for product in products:
            category_name = products['category']
            _category = Category.objects.filter(name=category_name).first()
            product['category'] = _category
            new_product = Product(**product)
            new_product.save()
