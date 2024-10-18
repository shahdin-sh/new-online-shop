from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseBadRequest, Http404
from django.shortcuts import render, get_object_or_404, redirect

from products.models import Discount
from cart.cart import Cart

from orders.models import Order
import requests, json


def payment_process(request):
    # Check if the token in the query params matches the session token
    payment_token = request.session.get('payment_token')
    if payment_token and payment_token == request.GET.get('token'):
        order_id = request.session['order_info']['order_id']
        order = Order.objects.get(id=order_id)
        rial_total_price = request.session['order_info']['rial_total_price']

        zarinpal_request_url = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"

        request_header = {
            "accept": "application/json",
            "content-type": "application/json",
        }

        request_data = {
            'merchant_id': settings.ZARINPAL_MERCHANT_ID,
            'amount': rial_total_price,
            'description': f'{order.id}: {order.customer.first_name}  {order.customer.last_name} order',
            'callback_url': "http://127.0.0.1:8000/payment/result",
        }

        response = requests.post(url=zarinpal_request_url, data=json.dumps(request_data), headers=request_header)

        data = response.json().get('data')

        errors = response.json().get('errors')

        if not errors:
            return redirect(f"https://sandbox.zarinpal.com/pg/StartPay/{data.get('authority')}")
        return HttpResponseBadRequest(f'Error from Zarinpal: {errors}')
    raise Http404()


@transaction.atomic
def payment_process_result(request):
    authority = request.GET.get('Authority')
    status = request.GET.get('Status')

    if status == 'OK':
        verify_request_url = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"

        request_header = {
            "accept": "application/json",
            "content-type": "application/json",
        }

        request_data = {
            'merchant_id': settings.ZARINPAL_MERCHANT_ID,
            'amount': request.session['order_info']['rial_total_price'],
            'authority': authority,
        }

        response = requests.post(url=verify_request_url, data=json.dumps(request_data), headers=request_header)
    
        data = response.json().get('data')

        if data['code'] == 100:
            # discount restriction for the user
            user_discounts = request.session.get('user_discounts')
            if user_discounts:
                for key, value in user_discounts.items():
                    discount_obj = Discount.objects.get(id=value.get('id'))

                    discount_obj.usage_by.set([request.user])
                    discount_obj.save()

            Cart(request).clear_the_cart()

            order = Order.objects.get(id=request.session['order_info']['order_id'])
            order.status = Order.ORDERS_STATUS_CHOICES[0]
            order.save()

            messages.success(request, f'payment succeeded your refid is {data['ref_id']}')
            return redirect('account:my_account')
        
        elif data['code'] == 101:
            messages.warning(request, 'payment has been done before')
            return request.META.get('HTTP_REFERER')
        
        else:
            return HttpResponseBadRequest(f'Error: {response.json().get('errors')}')
    elif status == 'NOK':
        messages.error(request, 'payment was unsuccessful, please try again')
        return redirect('orders:checkout')
    else:
        raise Http404()