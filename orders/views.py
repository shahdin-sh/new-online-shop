import logging
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.cart import Cart
from cart.decorators import item_in_cart_required
from orders.forms import CustomerWithAddressForm
from orders.models import OrderItem, Order


@item_in_cart_required
@login_required
def checkout(request):

    breadcrumb_data = [{'lable': 'checkout', 'title':'Checkout'}]

    context = {
        'customer_form': CustomerWithAddressForm(),
        'breadcrumb_data': breadcrumb_data,
    }
    
    return render(request, 'orders/checkout.html', context)


@login_required
def create_and_update_customer(request):
    current_user = request.user
    if request.method == 'POST':
        customer_form = CustomerWithAddressForm(request.POST, instance=current_user.customer_info)
        if customer_form.is_valid():
            create_new_customer = customer_form.save(commit=False)
            create_new_customer.user = current_user
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
def order_create(request):
    # check if user has a customer information or not
    current_user = request.user
    cart = Cart(request)

    if request.method == 'POST':

        if current_user.customer_info:

            # creating order and order item
            order_obj = Order.objects.create(
                customer = current_user.customer_info
            )

            for item in cart:
                product = item['product_obj']
                size = item['size']
                color = item['color']
                quantity = item['quantity']

                OrderItem.objects.create(
                    order = order_obj,
                    product = product,
                    size = size,
                    color = color,
                    quantity = quantity,
                    price = product.price,
                )

            # saving the order in the session for the paymant function
            request.session['order_id'] = order_obj.id

            cart.clear_the_cart()

            return redirect('paymant:paymant_process')
        else:
            return HttpResponse('please fill out your info and address form first, then submit your order.')
   