from django.shortcuts import render
from datetime import datetime

links_menu = [
    {'href': 'main:index', 'name': 'Home', 'active': ['index', ]},
    {'href':
        [
            {'href': 'main:category', 'name': 'Shop Category'},
            {'href': 'main:single-product', 'name': 'Product Details'}
        ],
        'name': 'Shop',
        'active': ['category', 'single-product'],
        'is_drop_down': True,
    },
    {'href': 'main:contact', 'name': 'Contact', 'active': ['contact', ]},
]

context = {
    'year': datetime.now().year,
    'links_menu': links_menu,
}


# Create your views here.
def main(request):
    context['title'] = 'Главная'
    return render(request, 'mainapp/index.html', context)


def category(request):
    context['title'] = 'Категории'
    return render(request, 'mainapp/category.html', context)


def contact(request):
    context['title'] = 'Контакты'
    return render(request, 'mainapp/contact.html', context)


def singleproduct(request):
    context['title'] = 'Товар'
    return render(request, 'mainapp/single-product.html', context)
