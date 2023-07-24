import functools
from django.shortcuts import redirect
from django.contrib import messages
from .cart import Cart
from products.models import Product
from django.shortcuts import get_object_or_404



def item_in_cart_required(view_func, redirect_url='products:product_categories'):
    """
        this decorator restricts users to access the cart, if there is no item in the cart and the massage
        is going to pop up on their screen and they wil redirect to shop_categories url and from this page they
        can add products to their cart.
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        cart = Cart(request)
        # Call the is_item method to check if the cart has any items
        if cart.is_item():
            return view_func(request, *args, **kwargs)
        messages.info(request, "There is no item in the cart")
        return redirect(redirect_url)  
    return wrapper