from django.shortcuts import render, HttpResponse
from .models import Category, Product
import json

with open('mainapp/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

links_menu = data['links_menu']
index_carousel = data['index_carousel']
# treding_product = data['treding_product']

context = {}


# Create your views here.
def main(request):
    treding_product = Product.objects.all()[:8]
    context['links_menu'] = links_menu
    context['title'] = 'Главная'
    context['index_carousel'] = index_carousel
    context['treding_product'] = treding_product
    context['best_sellers'] = treding_product
    return render(request, 'mainapp/index.html', context)


def category(request):
    categories = {p.category.name: len(Product.objects.all().filter(category_id__exact=p.category.id)) for p in Product.objects.all()}
    product = Product.objects.all()
    context['links_menu'] = links_menu
    context['title'] = 'Категории'
    context['products'] = product
    context['categories'] = categories
    return render(request, 'mainapp/category.html', context)


def contact(request):
    context['links_menu'] = links_menu
    context['title'] = 'Контакты'
    return render(request, 'mainapp/contact.html', context)


def singleproduct(request):
    product = Product.objects.first()
    context['links_menu'] = links_menu
    context['title'] = 'Товар'
    context['product'] = product
    return render(request, 'mainapp/productpage.html', context)


def productpage(request, pk):
    product = Product.objects.get(id__exact=pk)
    context['links_menu'] = links_menu
    context['title'] = product.name
    context['product'] = product
    return render(request, 'mainapp/productpage.html', context)
