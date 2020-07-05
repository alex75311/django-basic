from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
import json

from django.template.loader import render_to_string

from basketapp.models import Basket
from djangobasic.settings import LOGIN_URL
from mainapp.models import Product

with open('mainapp/json/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

links_menu = data['links_menu']


@login_required
def index(request):
    products = Basket.objects.filter(user=request.user)
    context = {
        'links_menu': links_menu,
        'title': 'Корзина',
        'products': products,
    }
    return render(request, 'basketapp/basket.html', context)


@login_required
def add(request, pk):
    if LOGIN_URL in request.META.get('HTTP_REFERER'):
        return redirect('product:product-page', pk=pk)
    product = get_object_or_404(Product, pk=pk)
    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)
    elif product.quantity > basket.quantity:
        basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove(request, pk):
    if request.is_ajax():
        basket = Basket.objects.filter(user=request.user, pk=pk).first()
        basket.delete()

        products = Basket.objects.filter(user=request.user)
        result = render_to_string('basketapp/includes/inc__basket_area.html', {'products': products})
    return JsonResponse({'result': result})


@login_required
def edit(request, pk, quantity):
    if request.is_ajax():
        basket = Basket.objects.filter(user=request.user, product=pk).first()
        if quantity > 0:
            if quantity <= basket.product.quantity:
                basket.quantity = quantity
            else:
                basket.quantity = basket.product.quantity
            basket.save()
        products = Basket.objects.filter(user=request.user)

        result = render_to_string('basketapp/includes/inc__basket_area.html', {'products': products})
        return JsonResponse({'result': result})
