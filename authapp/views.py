from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm, ShopUserChangePassword, UserProfileEditForm
from authapp.models import ShopUser, UserProfile


def login(request):
    activate_message = ''
    if request.method == 'POST':
        form = ShopUserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                redirect_url = request.GET.get('next')
                return HttpResponseRedirect(redirect_url) if redirect_url else HttpResponseRedirect(reverse('main:index'))
    else:
        try:
            if reverse('authapp:register') in request.META['HTTP_REFERER']:
                activate_message = 'На Ваш e-mail выслано письмо для подтверждения регистрации'
        except KeyError:
            pass

        form = ShopUserLoginForm()

    context = {
        'title': 'Вход в систему',
        'form': form,
        'activate_message': activate_message,
    }
    return render(request, 'authapp/login.html', context)


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))


def register(request):
    if request.method == 'POST':
        form = ShopUserRegisterForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            user.send_verify_mail()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        form = ShopUserRegisterForm()

    context = {
        'title': 'Регистрация',
        'form': form,
    }
    return render(request, 'authapp/register.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = UserProfileEditForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('auth:edit-profile'))
    else:
        form = ShopUserEditForm(instance=request.user)
        profile_form = UserProfileEditForm(instance=request.user.userprofile)

    context = {
        'title': 'Редактирование данных',
        'form': form,
        'profile_form': profile_form,
    }
    return render(request, 'authapp/edit.html', context)


@login_required
def change_password(request):
    pass


def verify(request, email, activation_key):
    user = ShopUser.objects.get(email=email)
    if user.activation_key == activation_key and not user.is_activation_key_expired():
        verify_message = 'Учетная запись активирована'
        user.is_active = True
        user.activation_key = ''
        user.save()
        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    else:
        verify_message = 'Учетная запись не активирована'
    context = {
        'verify_message': verify_message,
    }
    return render(request, 'authapp/verify.html', context)


@receiver(post_save, sender=ShopUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()
