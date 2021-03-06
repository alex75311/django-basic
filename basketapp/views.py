from django.contrib.auth.decorators import login_required
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from django.template.loader import render_to_string

from basketapp.models import Basket
from djangobasic.settings import LOGIN_URL
from mainapp.models import Product


@login_required
def index(request):
    context = {
        'title': 'Корзина',
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
    elif product.quantity > 0:
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
            if quantity <= basket.product.quantity + basket.quantity:
                basket.quantity = quantity
            else:
                basket.quantity = basket.product.quantity
            basket.save()
        basket = Basket.objects.filter(user=request.user)

        result = render_to_string('basketapp/includes/inc__basket_area.html', {'basket': basket})
        return JsonResponse({'result': result})


@receiver(pre_save, sender=Basket)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
    if instance.pk:
        instance.product.quantity -= instance.quantity - sender.get_item(instance.pk).quantity
    else:
        instance.product.quantity -= instance.quantity
    instance.product.save()


@receiver(pre_delete, sender=Basket)
def product_quantity_update_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()
