from django.urls import path, include, re_path
from .views import home_page, category_detail, product_detail_view

# The first element is the type and the second is the parameter name to use when calling the view. <slug:category_slug>
urlpatterns = [
    path('', home_page, name='homepage'),
    path('<slug:product_slug>', product_detail_view, name='product_detail')
    # path('<slug:slug>', category_detail, name='category_detail'),
]