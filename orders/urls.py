from django.urls import path, include, re_path
from orders.views import checkout, create_and_update_customer, order_create


app_name = 'orders'

urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    path('customer_create', create_and_update_customer, name='create_and_update_customer'),
    path('order_create', order_create, name='order_create')
]