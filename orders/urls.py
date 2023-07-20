from django.urls import path, include, re_path
from .views import checkout


app_name = 'orders'

urlpatterns = [
    path('checkout/', checkout, name='checkout'),
]