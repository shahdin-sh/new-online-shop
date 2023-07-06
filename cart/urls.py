from django.urls import path, include, re_path
from .views import cart_detail_view, add_product_to_the_cart


app_name = 'cart'

urlpatterns = [
    path('', cart_detail_view, name='cart_detail_view'),
    path('add/product/<int:product_id>', add_product_to_the_cart, name='add_to_cart')
]