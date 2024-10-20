from django.urls import path, include, re_path
from .views import homepage

# The first element is the type and the second is the parameter name to use when calling the view, <slug:category_slug>

app_name = 'pages'

urlpatterns = [
    path('', homepage, name='homepage')
]