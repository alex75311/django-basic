from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
import json
from django.urls import reverse
from authapp.forms import ShopUserLoginForm


with open('mainapp/json/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

links_menu = data['links_menu']


def login(request):
    if request.method == 'POST':
        form = ShopUserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = ShopUserLoginForm()

    context = {
        'title': 'Вход в систему',
        'form': form,
        'links_menu': links_menu,
    }
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))


def register(request):
    pass


def edit_profile(request):
    pass
