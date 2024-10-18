import logging, uuid
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.urls import reverse
from django.utils.translation import gettext as _
from cart.cart import Cart
from cart.decorators import item_in_cart_required
from orders.forms import CustomerWithAddressForm
from orders.models import OrderItem, Order, CustomerWithAddress
from products.models import Discount

# const values for breadcrumb data
breadcrumb_checkout = _('checkout')


@item_in_cart_required
@login_required
def checkout(request):

    breadcrumb_data = [{'lable': breadcrumb_checkout, 'title':breadcrumb_checkout}]

    context = {
        'customer_form': CustomerWithAddressForm(),
        'breadcrumb_data': breadcrumb_data,
    }
    
    return render(request, 'orders/checkout.html', context)


@login_required
def create_and_update_customer(request):
    current_user = request.user
    if request.method == 'POST':
        customer_form = CustomerWithAddressForm(request.POST)

        if customer_form.is_valid():
            create_new_customer = customer_form.save(commit=False)

            create_new_customer.user = current_user
            create_new_customer.first_name = current_user.first_name
            create_new_customer.last_name = current_user.last_name
            create_new_customer.email = current_user.email

            create_new_customer.save()

            if not current_user.customer_info:
                messages.success(request, f'your inforamtion and your address added successfully {current_user.username}.')
            else:
                messages.success(request, f'your inforamtion and your address updated successfully {current_user.username}.')

            #  redirect user to the current page
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            # Log form errors
            logger = logging.getLogger(__name__)
            logger.error("Form validation failed: %s", customer_form.errors)
    else:
        customer_form = CustomerWithAddressForm()
   

@login_required
@transaction.atomic
def order_create(request):
    # check if user has a customer information or not
    current_user = request.user
    cart = Cart(request)

    if request.method == 'POST':
        if CustomerWithAddress.objects.filter(user=current_user).exists():
            # creating order
            order_obj = Order.objects.create(
                customer = current_user.customer_info
            )

            for item in cart:
                product = item['product_obj']
                size = item['size']
                color = item['color']
                quantity = item['quantity']
                discounted_price = item.get('discounted_price', 0)

                # creating order item for each item in cart
                OrderItem.objects.create(
                    order = order_obj,
                    product = product,
                    size = size,
                    color = color,
                    quantity = quantity,
                    price = product.price,
                    discounted_price = discounted_price
                )

            # saving the order and order total price in the session for the payment function
            order_info = request.session['order_info'] = {} 
            order_info['order_id'] = order_obj.id
            order_info['rial_total_price'] = order_obj.get_order_total_price * 10

            # secure the payment process
            payment_token = str(uuid.uuid4())
            request.session['payment_token'] = payment_token
            return redirect(reverse('payment:payment_process') + f'?token={payment_token}')
        else:
            return HttpResponse('please fill out your info and address form first, then submit your order.')