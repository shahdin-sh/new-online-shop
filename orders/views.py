from django.shortcuts import render, redirect, HttpResponse, get_object_or_404, reverse
from .forms import OrderForm
from .models import OrderItem, Order
from cart.decorators import item_in_cart_required
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.contrib import messages
from django.db import IntegrityError
import logging


@item_in_cart_required
@login_required
def checkout(request):
    breadcrumb_data = [{'lable': 'checkout', 'title':'Checkout'}]

    context = {
        'order_form': OrderForm(),
        'breadcrumb_data': breadcrumb_data
    }
    
    return render(request, 'orders/checkout.html', context)


# we create order an order item with this view.
@login_required
def order_create(request):
    user = request.user
    try:
        order = Order.objects.get(customer=user)
    except Order.DoesNotExist:
        order = None
    if request.method == 'POST':
        order_form = OrderForm(request.POST, instance=order)
        if order_form.is_valid():
            order_obj = order_form.save(commit=False)
            order_obj.customer = user
            order_obj.save()
            # save the user informations.
            user.first_name = order_obj.first_name
            user.last_name = order_obj.last_name
            user.email = order_obj.email
            user.save()
            if order:
                messages.success(request, 'your informations updated successfully')
            else:
                messages.success(request, 'your informations created successfully')
        else:
             # Log form errors
            logger = logging.getLogger(__name__)
            logger.error("Form validation failed: %s", order_form.errors)
            
    else:
        order_form = OrderForm()
    # redirect user to the current page
    return redirect(request.META.get('HTTP_REFERER'))
   

@login_required
def order_item_create(request):
    user = request.user
    # check if user fiil out order form or not.
    try:
        order = Order.objects.get(customer=user)
    except Order.DoesNotExist:
        order = None
    if order:
        cart = Cart(request)
        # getting product variant from the cart.
        for item in cart:
            product = item['product_obj']
            size = item['size']
            color = item['color']
            quantity = item['quantity']
            OrderItem.objects.create(
                order = get_object_or_404(Order.objects.filter(customer=user)),
                product = product,
                size = size,
                color = color,
                quantity = quantity,
                price = product.price,
                )
            # update the current product quantity
            product.quantity = item['current_product_stock']
            product.save()
        cart.clear_the_cart()
        return redirect('paymant:paymant_process')
    else:
        return HttpResponse('please fill out your order information form first')
    
        
        