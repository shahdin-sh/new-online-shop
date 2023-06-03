from django.urls import path, include, re_path
from .views import cart_detail_view


urlpatterns = [
    path('', cart_detail_view, name='cart_detail_view')
]