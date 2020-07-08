from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from adminapp.forms import AdminShopCreateUser, AdminEditUserProfile, AdminCategoryCreate, AdminProductCreate, \
    AdminCategoryEdit, AdminProductEdit
from authapp.models import ShopUser
from mainapp.models import Product, Category
import json

with open('adminapp/json/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

links_menu = data['links_menu']


@user_passes_test(lambda x: x.is_superuser)
def user_create(request):
    if request.method == 'POST':
        form = AdminShopCreateUser(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:users'))
    else:
        form = AdminShopCreateUser()

    context = {
        'title': 'создать пользователя',
        'form': form,
        'links_menu': links_menu,
    }
    return render(request, 'adminapp/create.html', context)


@user_passes_test(lambda x: x.is_superuser)
def users(request):
    users_list = ShopUser.objects.all().order_by('-is_active', '-is_staff', 'username')

    context = {
        'title': 'Пользователи',
        'object_list': users_list,
        'links_menu': links_menu,
    }
    return render(request, 'adminapp/users.html', context)


@user_passes_test(lambda x: x.is_superuser)
def user_edit(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        form = AdminEditUserProfile(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:users'))
    else:
        form = AdminEditUserProfile(instance=user)

    context = {
        'form': form,
        'title': 'Редактирование пользователя',
        'links_menu': links_menu,
        'image': user.avatar,
    }
    return render(request, 'adminapp/edit.html', context)


@user_passes_test(lambda x: x.is_superuser)
def user_delete(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()
    return HttpResponseRedirect(reverse('adminapp:users'))


@user_passes_test(lambda x: x.is_superuser)
def product(request, page=1):
    product_list = Product.objects.all().order_by('-is_active', 'name')
    for el in product_list:
        el.description = el.description[:100]

    paginator = Paginator(product_list, 2)
    try:
        page_paginator = paginator.page(page)
    except PageNotAnInteger:
        page_paginator = paginator.page(1)
    except EmptyPage:
        page_paginator = paginator.page(page_paginator.num_pages)
    context = {
        'title': 'продукты',
        'object_list': page_paginator,
        'links_menu': links_menu,
    }
    return render(request, 'adminapp/product.html', context)


@user_passes_test(lambda x: x.is_superuser)
def product_edit(request, pk):
    el = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = AdminProductEdit(request.POST, request.FILES, instance=el)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:product', pk=pk))
    else:
        form = AdminProductEdit(instance=el)
    context = {
        'title': 'Редактирование товара',
        'links_menu': links_menu,
        'form': form,
        'image': el.image,
    }
    return render(request, 'adminapp/edit.html', context)


@user_passes_test(lambda x: x.is_superuser)
def product_delete(request, pk):
    el = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        el.is_active = not el.is_active
        el.save()
    return HttpResponseRedirect(reverse('adminapp:product'))


@user_passes_test(lambda x: x.is_superuser)
def product_create(request):
    if request.method == 'POST':
        form = AdminProductCreate(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:product'))
    else:
        form = AdminProductCreate()
        context = {
            'form': form,
            'title': 'Создать товар',
            'links_menu': links_menu,
        }
    return render(request, 'adminapp/create.html', context)


@user_passes_test(lambda x: x.is_superuser)
def category(request):
    category_list = Category.objects.all().order_by('name')
    context = {
        'title': 'Категории',
        'object_list': category_list,
        'links_menu': links_menu,
    }
    return render(request, 'adminapp/category.html', context)


@user_passes_test(lambda x: x.is_superuser)
def category_edit(request, pk):
    el = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = AdminCategoryEdit(request.POST, request.FILES, instance=el)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:category'))
    else:
        form = AdminCategoryEdit(instance=el)
    context = {
        'title': 'Редактирование товара',
        'links_menu': links_menu,
        'form': form,
    }
    return render(request, 'adminapp/edit.html', context)


@user_passes_test(lambda x: x.is_superuser)
def category_delete(request, pk):
    el = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        product_list = el.product_set.all()
        el.is_active = not el.is_active
        el.save()
        for prod in product_list:
            prod.is_active = el.is_active
            prod.save()
    return HttpResponseRedirect(reverse('adminapp:category'))


@user_passes_test(lambda x: x.is_superuser)
def category_create(request):
    if request.method == 'POST':
        form = AdminCategoryCreate(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:category'))
    else:
        form = AdminCategoryCreate()
        context = {
            'form': form,
            'title': 'Создать категорию',
            'links_menu': links_menu,
        }
    return render(request, 'adminapp/create.html', context)
