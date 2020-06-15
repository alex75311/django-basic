from django.shortcuts import render
from datetime import datetime

context = {
    'year': datetime.now().year,
}


# Create your views here.
def main(request):
    context['title'] = 'Главная'

    return render(request, 'mainapp/index.html', context)


def category(request):
    context['title'] = 'Категории'

    return render(request, 'mainapp/category.html', context)


def contact(request):
    context['title'] = 'Контакты'

    return render(request, 'mainapp/contact.html', context)


def singleproduct(request):
    context['title'] = 'Товар'

    return render(request, 'mainapp/single-product.html', context)
