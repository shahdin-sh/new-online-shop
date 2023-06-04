from django.shortcuts import render, redirect, get_object_or_404
from .cart import Cart
from .forms import AddToCartForm
from products.models import Product


def cart_detail_view(request):
    context = {
        'cart': Cart(request),
    }
    print(Cart(request))
    return render(request, 'cart_detail_view.html', context)


def add_product_to_the_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product.is_active_manager, product_id)
    cart_form = AddToCartForm(request.POST)
    if cart_form.is_valid():
        cleaned_data = cart_form.cleaned_data
        quantity = cleaned_data['quantity']
        cart.add_to_cart(product, quantity)
    return redirect('cart:cart_detail_view')