from django.shortcuts import render, get_object_or_404
from orders.models import Order
import requests, json
from django.conf import settings


def paymant_process(request):
    order = get_object_or_404(Order.objects.filter(customer=request.user))
    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    zarinpal_request_url = "https://api.zarinpal.com/pg/v4/payment/request.json"

    request_header = {
        "accept": "application/json",
        "content-type": "application/json",
    }

    request_data = {
        'merchant_id': settings.ZARINPAL_MERCHANT_ID,
        'amount': rial_total_price,
        'description': f'{order.id}: {order.first_name}  {order.last_name} order',
        'callback_url': 'http://127.0.0.1:8000',
    }

    response = requests.post(url=zarinpal_request_url, data=json.dumps(request_data), headers=request_header)
    print(f"your response is {response.json()['data']}")