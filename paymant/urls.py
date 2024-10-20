from django.urls import path, include, re_path
from paymant.views import payment_process, payment_process_result

# The first element is the type and the second is the parameter name to use when calling the view, <slug:category_slug>

app_name = 'payment'

urlpatterns = [
    path('', payment_process, name='payment_process'),
    path('result', payment_process_result, name='payment_result')
]