from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
import json

from django.urls import reverse

from basketapp.models import Basket
from mainapp.models import Product

with open('mainapp/json/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

links_menu = data['links_menu']


def index(request):
    if not request.user.username:
        return HttpResponseRedirect(reverse('auth:login'))
    else:
        products = Basket.objects.filter(user=request.user)
    context = {
        'links_menu': links_menu,
        'title': 'Корзина',
        'products': products,
    }
    return render(request, 'basketapp/basket.html', context)


def add(request, pk):
    if not request.user.username:
        return HttpResponseRedirect(reverse('auth:login'))

    product = get_object_or_404(Product, pk=pk)
    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)
    else:
        basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove(request, pk):
    basket = Basket.objects.filter(user=request.user, pk=pk).first()
    basket.quantity -= 1
    basket.save()

    if basket.quantity == 0:
        basket.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
