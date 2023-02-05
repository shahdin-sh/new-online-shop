from django.urls import path, include, re_path
from .views import home_page, category_detail

urlpatterns = [
    path('', home_page, name='homepage'),
    path('<slug:slug>', category_detail, name='category_detail'),
]