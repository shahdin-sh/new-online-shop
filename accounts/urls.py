from django.urls import path, include, re_path
from .views import wishlist_view, my_account


app_name = 'account'

urlpatterns = [
    path('wishlist/', wishlist_view, name='wishlist_view'),
    path('my_account/', my_account, name="my_account"),
]