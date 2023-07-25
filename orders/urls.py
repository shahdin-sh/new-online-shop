from django.urls import path, include, re_path
from .views import checkout, order_create


app_name = 'orders'

urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    path('order_create', order_create, name='order_create')
]