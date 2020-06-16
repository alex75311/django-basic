from django.shortcuts import render
from datetime import datetime
import json

with open('mainapp/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

links_menu = data['links_menu']
index_carousel = data['index_carousel']
treding_product = data['treding_product']

context = {
    'year': datetime.now().year,
    'links_menu': links_menu,
}


# Create your views here.
def main(request):
    context['title'] = 'Главная'
    context['index_carousel'] = index_carousel
    context['treding_product'] = treding_product
    context['best_sellers'] = treding_product
    return render(request, 'mainapp/index.html', context)


def category(request):
    context['title'] = 'Категории'
    context['products'] = treding_product
    return render(request, 'mainapp/category.html', context)


def contact(request):
    context['title'] = 'Контакты'
    return render(request, 'mainapp/contact.html', context)


def singleproduct(request):
    context['title'] = 'Товар'
    return render(request, 'mainapp/single-product.html', context)
