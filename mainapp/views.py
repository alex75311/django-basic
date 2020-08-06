from django.core.cache import cache
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page

from djangobasic.settings import LOW_CACHE
from .models import Product, Category

context = {}


def main(request):
    context['title'] = 'Главная'
    return render(request, 'mainapp/index.html', context)


def get_category():
    product = Product.objects.exclude(is_active=False).exclude(quantity=0).select_related()
    category = Category.objects.exclude(is_active=False)
    categories = {c: c.product_set.exclude(is_active=False).exclude(quantity=0).count()
                  for c in category}
    context['products'] = product
    context['categories'] = categories
    return context


def category(request):
    if LOW_CACHE:
        key = 'category'
        context = cache.get(key)
        if context is None:
            context = get_category()
            cache.set(key, context)
    else:
        context = get_category()
    context['title'] = 'Категории'
    return render(request, 'mainapp/category.html', context)


@cache_page(3600)
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


def get_category_id(pk):
    categories = {p.category: Product.objects.all() for p in Product.objects.all()}
    if pk == 0:
        product = Product.objects.exclude(is_active=False).exclude(quantity=0)
    else:
        this_category = get_object_or_404(Category, pk=pk)
        product = this_category.product_set.exclude(is_active=False).exclude(quantity=0)
    context['products'] = product
    context['categories'] = categories
    return context


def category_id(request, pk):
    if LOW_CACHE:
        key = f'category_{pk}'
        context = cache.get(key)
        if context is None:
            context = get_category_id(pk)
            cache.set(key, context)
    else:
        context = get_category_id(pk)

    result = render_to_string('mainapp/includes/inc__product_category.html', context)
    return JsonResponse({'result': result})


def product_ajax(request, pk):
    if request.is_ajax():
        product_price = Product.objects.get(pk=pk).price
        return JsonResponse({'product_price': product_price})
