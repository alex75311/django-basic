from django.urls import path
import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    # path('users/create/', adminapp.user_create, name='user_create'),
    path('users/create/', adminapp.UserCreateView.as_view(), name='user_create'),
    # path('users/read/', adminapp.users, name='users'),
    path('users/read/', adminapp.UserReadView.as_view(), name='users'),
    # path('users/edit/<int:pk>/', adminapp.user_edit, name='user_edit'),
    path('users/edit/<int:pk>/', adminapp.UserEditView.as_view(), name='user_edit'),
    # path('users/delete/<int:pk>/', adminapp.user_delete, name='user_delete'),
    path('users/delete/<int:pk>/', adminapp.UserDeleteView.as_view(), name='user_delete'),

    # path('product/read/', adminapp.product, name='product'),
    path('product/read/', adminapp.ProductReadView.as_view(), name='product'),
    # path('product/read/<int:page>/', adminapp.product, name='product_page'),
    path('product/read/<int:page>/', adminapp.ProductReadView.as_view(), name='product_page'),
    path('product/create/', adminapp.product_create, name='product_create'),
    path('product/delete/<int:pk>/', adminapp.product_delete, name='product_delete'),
    path('product/edit/<int:pk>/', adminapp.product_edit, name='product_edit'),

    path('category/', adminapp.category, name='category'),
    path('category/delete/<int:pk>/', adminapp.category_delete, name='category_delete'),
    path('category/edit/<int:pk>', adminapp.category_edit, name='category_edit'),
    path('category/create/', adminapp.category_create, name='category_create'),

    path('order/read/', adminapp.OrdersReadView.as_view(), name='orders'),
    path('order/update/<int:pk>', adminapp.OrderUpdateView.as_view(), name='order_update'),
    path('order/update/item/<int:pk>', adminapp.OrderItemUpdateView.as_view(), name='update_order_item'),
]
