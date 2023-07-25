from django.shortcuts import render, redirect, HttpResponse
from .forms import OrderForm
from .models import OrderItem
from accounts.models import CustomUserModel
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.contrib import messages
from django.db import IntegrityError


def checkout(request):
    context = {
        'order_form': OrderForm()
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def order_create(request):
    try:
        cart  = Cart(request)
        if request.method == 'POST':
            order_form = OrderForm(request.POST)
            if order_form.is_valid():
                order_obj = order_form.save(commit=False)
                order_obj.customer = request.user
                order_obj.save()
                for item in cart:
                    product = item['product_obj']
                    OrderItem.objects.create(
                        order = order_obj,
                        product = product,
                        quantity = item['quantity'],
                        price = product.price,
                    )
                cart.clear_the_cart()
                messages.success(request, 'your order submited successfully')
        else:
            order_form = OrderForm()
        # redirect user to the current page
        return redirect(request.META.get('HTTP_REFERER'))
    # this error would cause if the current user wants to create an order twice (OnetoOnefield defined for customer in models.py)
    except IntegrityError:
        return HttpResponse(f'You have already create an order {request.user}', status=404)
