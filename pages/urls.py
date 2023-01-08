from django.urls import path, include, re_path
from .views import HomePageView


urlpatterns = [
    path('', HomePageView.as_view(), name='homepage')
]