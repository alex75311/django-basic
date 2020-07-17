from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from .models import Product, Category

context = {}


def main(request):
    context['title'] = 'Главная'
    return render(request, 'mainapp/index.html', context)


def category(request):
    categories = {p.category: Product.objects.filter(category_id__exact=p.category.id).exclude(is_active=False).count()
                  for p in Product.objects.exclude(is_active=False)}
    product = Product.objects.exclude(is_active=False)
    context['products'] = product
    context['categories'] = categories
    return render(request, 'mainapp/category.html', context)


def contact(request):
    context['title'] = 'Контакты'
    return render(request, 'mainapp/contact.html', context)


def singleproduct(request):
    product = Product.objects.first()
    context['title'] = 'Товар'
    context['product'] = product
    return render(request, 'mainapp/productpage.html', context)


def productpage(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context['title'] = product.name
    context['product'] = product
    return render(request, 'mainapp/productpage.html', context)


def category_id(request, pk):
    categories = {p.category: Product.objects.all() for p in Product.objects.all()}
    if pk == 0:
        product = Product.objects.exclude(is_active=False)
    else:
        this_category = get_object_or_404(Category, pk=pk)
        product = this_category.product_set.exclude(is_active=False)
    context['title'] = 'Категории'
    context['products'] = product
    context['categories'] = categories

    result = render_to_string('mainapp/includes/inc__product_category.html', context)
    return JsonResponse({'result': result})
