from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .forms import OrderForm
from .models import OrderItem, Order
from cart.decorators import item_in_cart_required
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.contrib import messages
from django.db import IntegrityError


@item_in_cart_required
def checkout(request):
    context = {
        'order_form': OrderForm(),
    }
    return render(request, 'orders/checkout.html', context)

# we create order an order item with this view.
@login_required
def order_create(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order_obj = order_form.save(commit=False)
            order_obj.customer = request.user
            order_obj.save()
    else:
        order_form = OrderForm()
    # redirect user to the current page
    return redirect(request.META.get('HTTP_REFERER'))
   

# this function only update the values of order form and order item will be created from upper view.
@login_required
def order_update(request):
    if request.user.order:
        if request.method == 'POST':
            order_form = OrderForm(request.POST)
            if order_form.is_valid():
                Order.objects.filter(customer=request.user).delete()
                order_obj = order_form.save(commit=False)
                order_obj.customer = request.user
                order_obj.save()
                messages.success(request, 'your informations updated successfully')
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            order_form - OrderForm()

@login_required
def order_item_create(request):
    user_order = Order.objects.filter(customer=request.user)
    if user_order.exists():
        cart = Cart(request)
        for item in cart:
            product = item['product_obj']
            OrderItem.objects.create(
                order = get_object_or_404(user_order),
                product = product,
                quantity = item['quantity'],
                price = product.price,
            )
            cart.clear_the_cart()
            messages.success(request, 'developing purchase section has not been completed yet')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponse('please fill out your order information form first')
    
        
        