import json
import os

from django.core.cache import cache

from basketapp.models import Basket
from djangobasic.settings import BASE_DIR, LOW_CACHE
from mainapp.models import Product


def get_content():
    with open(os.path.join(BASE_DIR, 'mainapp', 'json', 'data.json'), 'r', encoding='utf-8') as f:
        data = json.load(f)

    links_menu = data['links_menu']
    index_carousel = data['index_carousel']
    treding_product = Product.objects.all().select_related()[:8]

    contents = {
        'links_menu': links_menu,
        'index_carousel': index_carousel,
        'treding_product': treding_product,
        'best_sellers': treding_product,
    }
    return contents


def content(request):
    if LOW_CACHE:
        key = 'content'
        contents = cache.get(key)
        if contents is None:
            contents = get_content()
            cache.set(key, contents)
        return contents

    else:
        contents = get_content()
        return contents


def get_basket(request):
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    return {
        'basket': basket,
    }
