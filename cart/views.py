from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import AddToCartForm
from products.models import Product


def cart_detail_view(request):
    context = {
        'cart': Cart(request),
        'cart_len': Cart.__len__
    }
    print(request.session['cart'])
    return render(request, 'cart_detail_view.html', context)


def add_product_to_the_cart(request, product_id):
    cart = Cart(request)
    products = Product.is_active_manager.filter(is_featured=False)
    product = get_object_or_404(products, id=product_id)
    cart_form = AddToCartForm(request.POST, product_stock=product.quantity)
    if cart_form.is_valid():
        # getting quantity from input that fill by the user
        cleaned_data = cart_form.cleaned_data
        quantity = cleaned_data['quantity']
        cart.add_to_cart(product, quantity)
    return redirect('cart:cart_detail_view')


def remove_prodcut_from_the_cart(request, product_id):
    cart = Cart(request)
    products = Product.is_active_manager.filter(is_featured=False)
    product = get_object_or_404(products, id=product_id)
    cart.remove_from_the_cart(product)
    return redirect('cart:cart_detail_view')