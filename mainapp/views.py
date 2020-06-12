from django.shortcuts import render


# Create your views here.
def main(request):
    return render(request, 'mainapp/index.html')


def category(request):
    return render(request, 'mainapp/category.html')


def contact(request):
    return render(request, 'mainapp/contact.html')


def singleproduct(request):
    return render(request, 'mainapp/single-product.html')
