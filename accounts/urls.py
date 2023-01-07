from django.urls import path, include, re_path
from .views import signup_view


urlpatterns = [
    path('signup/', signup_view, name='signup')
]