from django.urls import path, include, re_path
from cart.views import cart_detail_view, add_product_to_the_cart, remove_product_from_the_cart, clear_the_cart, apply_discount_for_cart_items


app_name = 'cart'

urlpatterns = [
    path('' , cart_detail_view, name='cart_detail_view'),
    path('add/product/<int:product_id>', add_product_to_the_cart, name='add_to_cart'),
    path('remove/product/<int:product_id>', remove_product_from_the_cart, name='remove_from_the_cart'),
    path('clear', clear_the_cart, name="clear_the_cart"),
    path('apply_discount', apply_discount_for_cart_items, name='apply_discount')
]
