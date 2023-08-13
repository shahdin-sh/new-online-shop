from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .forms import OrderForm
from .models import OrderItem, Order
from cart.decorators import item_in_cart_required
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.contrib import messages
from django.db import IntegrityError
import logging


@item_in_cart_required
def checkout(request):
    context = {
        'order_form': OrderForm(),
    }
    return render(request, 'orders/checkout.html', context)

# we create order an order item with this view.
@login_required
def order_create(request):
    user_order = request.user.order
    user = request.user
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            print('something')
            # if user already had order delete the previous order and create another
            if user_order:
                Order.objects.filter(customer=user).delete()
            order_obj = order_form.save(commit=False)
            order_obj.customer = user
            order_obj.save()
            # save the firstname, lastname and email in user account every time user changes his order form.
            user.first_name = order_obj.first_name
            user.last_name = order_obj.last_name
            user.email = order_obj.email
            user.save()
            if not user_order:
                messages.success(request, 'your informations added successfully')
            messages.success(request, 'your informations updated successfully')
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
    user_order = Order.objects.filter(customer=request.user)
    if user_order.exists():
        cart = Cart(request)
        for item in cart:
            product = item['product_obj']
            quantity = item['quantity']
            order_obj = OrderItem.objects.create(
                        order = get_object_or_404(user_order),
                        product = product,
                        quantity = quantity,
                        price = product.price,
                        )
            cart.clear_the_cart()
            request.session['order_id'] = order_obj.id
            return redirect('account:my_account')
    else:
        return HttpResponse('please fill out your order information form first')
    
        
        