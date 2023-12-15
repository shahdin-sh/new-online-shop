from django.urls import path, include, re_path
from paymant.views import paymant_process

# The first element is the type and the second is the parameter name to use when calling the view, <slug:category_slug>

app_name = 'paymant'

urlpatterns = [
    path('', paymant_process, name='paymant_process'),
]