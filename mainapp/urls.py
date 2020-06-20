from django.urls import path
import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.main, name='index'),
    path('category/', mainapp.category, name='category'),
    path('contact/', mainapp.contact, name='contact'),
    path('single-product/', mainapp.singleproduct, name='single-product'),
    path('<int:pk>', mainapp.productpage, name='product-page'),
]
