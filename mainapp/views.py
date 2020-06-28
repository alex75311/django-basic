from django.shortcuts import render, get_object_or_404
from .models import Product, Category
import json

with open('mainapp/json/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

links_menu = data['links_menu']
index_carousel = data['index_carousel']

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
    categories = {p.category: Product.objects.all().filter(category_id__exact=p.category.id).count() for p in Product.objects.all()}
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
    product = get_object_or_404(Product, pk=pk)
    context['links_menu'] = links_menu
    context['title'] = product.name
    context['product'] = product
    return render(request, 'mainapp/productpage.html', context)


def category_id(request, pk):
    categories = {p.category: Product.objects.all().filter(category_id__exact=p.category.id).count() for p in
                  Product.objects.all()}
    if pk == 0:
        product = Product.objects.all()
    else:
        this_category = get_object_or_404(Category, pk=pk)
        product = this_category.product_set.all()
    context['links_menu'] = links_menu
    context['title'] = 'Категории'
    context['products'] = product
    context['categories'] = categories
    return render(request, 'mainapp/category.html', context)
