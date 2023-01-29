from django.urls import path, include, re_path
from .views import products_list_view, product_detail_view


urlpatterns = [
    path('', products_list_view, name='products_list_view'),
    path('<int:pk>', product_detail_view, name='product_detail_view'),
]