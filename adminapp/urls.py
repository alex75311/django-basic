from django.urls import path
import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('users/create/', adminapp.user_create, name='user_create'),
    path('users/read/', adminapp.users, name='users'),
    path('users/edit/<int:pk>/', adminapp.user_edit, name='user_edit'),
    path('users/delete/<int:pk>/', adminapp.user_delete, name='user_delete'),

    path('product/read/', adminapp.product, name='product'),
    path('product/read/<int:page>/', adminapp.product, name='product_page'),
    path('product/create/', adminapp.product_create, name='product_create'),
    path('product/delete/<int:pk>/', adminapp.product_delete, name='product_delete'),
    path('product/edit/<int:pk>/', adminapp.product_edit, name='product_edit'),

    path('category/', adminapp.category, name='category'),
    path('category/delete/<int:pk>/', adminapp.category_delete, name='category_delete'),
    path('category/edit/<int:pk>', adminapp.category_edit, name='category_edit'),
    path('category/create/', adminapp.category_create, name='category_create'),
]
