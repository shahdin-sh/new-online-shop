from django.urls import path, include, re_path
from .views import home_page, shop_categories, product_detail_view, add_to_wishlist, remove_from_wishlist, products_or_category_detail

# The first element is the type and the second is the parameter name to use when calling the view, <slug:category_slug>
urlpatterns = [
    path('', home_page, name='homepage'),
    path('shop_categories/', shop_categories, name='product_categories'),
    path('shop_categories/<slug:category_slug>', products_or_category_detail, name='category_detail'),
    path('shop_categories/<slug:category_slug>/<slug:product_slug>', product_detail_view, name='product_detail'),
    path('<slug:product_slug>/add_to_wishlist', add_to_wishlist, name='add_to_wishlist'),
    path('<slug:product_slug>/remove_from_wishlist', remove_from_wishlist, name='remove_from_wishlist')
]