import json

from basketapp.models import Basket
from mainapp.models import Product


def content(request):
    with open('mainapp/json/data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    links_menu = data['links_menu']
    index_carousel = data['index_carousel']
    treding_product = Product.objects.all()[:8]

    return {
        'links_menu': links_menu,
        'index_carousel': index_carousel,
        'treding_product': treding_product,
        'best_sellers': treding_product,
    }


def get_basket(request):
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    return {
        'basket': basket,
    }
