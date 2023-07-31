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
    user_order = request.user.order
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            # if user already had order delete the previous order and create another
            if user_order:
                Order.objects.filter(customer=request.user).delete()
            order_obj = order_form.save(commit=False)
            order_obj.customer = request.user
            order_obj.save()
            request.user.first_name = order_obj.first_name
            request.user.last_name = order_obj.last_name
            request.user.save()
        if not user_order:
            messages.success(request, 'your informations added successfully')
        messages.success(request, 'your informations updated successfully')
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
    
        
        