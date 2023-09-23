from django.urls import path, include, re_path
from .views import blog_grid


app_name = 'blog'

urlpatterns = [
    path('', blog_grid, name='blog_gird'),
]