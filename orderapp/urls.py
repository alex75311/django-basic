from django.urls import path
import orderapp.views as orderapp

app_name = 'orderapp'

urlpatterns = [
    path('', orderapp.UserOrderList.as_view(), name='index'),
    path('order-create/', orderapp.UserOrderCreate.as_view(), name='order_create'),
    path('order-update/<int:pk>', orderapp.UserOrderUpdate.as_view(), name='order_update'),
    path('order-delete/<int:pk>', orderapp.UserOrderDelete.as_view(), name='order_delete'),
    path('order-confirm/<int:pk>', orderapp.order_confirm, name='order_confirm'),
]
