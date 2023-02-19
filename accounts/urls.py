from django.urls import path, include, re_path
from .views import wishlist_view


urlpatterns = [
    path('wishlist/', wishlist_view, name='wishlist_view'),
]