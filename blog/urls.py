from django.urls import path
from blog.views import blog_grid, post_detail, tag_detail_view, category_detail_view


app_name = 'blog'

urlpatterns = [
    path('', blog_grid, name='blog_gird'),
    path('<slug:slug>', post_detail, name='post_detail'),
    path('tag/<slug:tag_slug>/', tag_detail_view, name='tag_detail_view'),
    path('category/<slug:category_slug>', category_detail_view, name='category_detail_view'),
    
]