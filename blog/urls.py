from django.urls import path, include, re_path
from .views import blog_grid, post_detail, tag_detail_view


app_name = 'blog'

urlpatterns = [
    path('', blog_grid, name='blog_gird'),
    path('<slug:slug>', post_detail, name='post_detail'),
    path('tag/<slug:tag_slug>/', tag_detail_view, name='tag_detail_view'),
]