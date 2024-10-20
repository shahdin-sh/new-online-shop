from django.urls import path, include, re_path
from products.views import *

# The first element is the type and the second is the parameter name to use when calling the view, <slug:category_slug>

app_name = 'products'

urlpatterns = [
    path('', shop_categories, name='product_categories'),
    path('<slug:product_slug>', product_detail_view, name='product_detail'), 
    path('<slug:product_slug>/add_to_wishlist', add_to_wishlist, name='add_to_wishlist'),
    path('<slug:product_slug>/remove_from_wishlist', remove_from_wishlist, name='remove_from_wishlist'),
    path('shop_categories/<slug:category_slug>', products_or_category_detail, name='category_detail'),
]