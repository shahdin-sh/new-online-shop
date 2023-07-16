from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import AddToCartForm
from products.models import Product


def cart_detail_view(request):
    cart = Cart(request)
    print(request.session['cart'])
    for item in cart:
        item['update_quantity_of_the_current_form'] = AddToCartForm(
            product_stock = item['product_obj'].quantity,
            initial = {
                'quantity' : item['quantity'],
                'inplace': True,
            }
            )
    context = {
        'cart': cart,
    }
    # print(request.session['cart'])
    return render(request, 'cart_detail_view.html', context)


# we use this view as action of our forms in 'cart_detail_view' and 'product_detail_view'
def add_product_to_the_cart(request, product_id):
    cart = Cart(request)
    products = Product.is_active_manager.filter(is_featured=False)
    product = get_object_or_404(products, id=product_id)
    cart_form = AddToCartForm(request.POST, product_stock=product.quantity)
    if cart_form.is_valid():
        # getting quantity from input that fill by the user
        cleaned_data = cart_form.cleaned_data
        quantity = cleaned_data['quantity']
        replace_current_quantity = cleaned_data['inplace']
        cart.add_to_cart(product, quantity, replace_current_quantity)
    return redirect('cart:cart_detail_view')


def remove_product_from_the_cart(request, product_id):
    cart = Cart(request)
    products = Product.is_active_manager.filter(is_featured=False)
    product = get_object_or_404(products, id=product_id)
    cart.remove_from_the_cart(product)
    return redirect('cart:cart_detail_view')