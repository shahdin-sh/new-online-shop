from django.urls import path, include, re_path
from .views import blog_grid, post_detail


app_name = 'blog'

urlpatterns = [
    path('', blog_grid, name='blog_gird'),
    path('<slug:slug>', post_detail, name='post_detail'),
]