from django.shortcuts import render, redirect, get_object_or_404, reverse
from .cart import Cart
from .decorators import item_in_cart_required
from .forms import AddToCartForm
from products.models import Product
import logging


@item_in_cart_required
def cart_detail_view(request):
    cart = Cart(request)
    print(request.session['cart'])

    for item in cart:
        item['update_quantity_of_the_current_form'] = AddToCartForm(
            product_stock=item['product_obj'].quantity, 
            initial = {
                'quantity': item['quantity'],
                'inplace': True,
                'size': item['size'],
                'color': item['color'],
            }
            )
    context = {
        'cart': cart,
    }
    return render(request, 'cart_detail_view.html', context)


# we use this view as action of our forms in 'cart_detail_view' and 'product_detail_view'
def add_product_to_the_cart(request, product_id):
    cart = Cart(request)
    products = Product.objects.filter(is_featured=False)
    product = get_object_or_404(products, id=product_id)
    cart_form = AddToCartForm(request.POST, product_stock=product.quantity)
    if cart_form.is_valid():
        # getting product variant from input that fill by the user
        cleaned_data = cart_form.cleaned_data
        quantity = cleaned_data.get('quantity', 1)
        size = cleaned_data.get('size')
        color = cleaned_data.get('color')
        replace_current_quantity = cleaned_data['inplace']
        cart.add_to_cart(product, size=size, color=color, quantity=quantity, replace_current_quantity=replace_current_quantity)
    else:
        # Log form errors
        logger = logging.getLogger(__name__)
        logger.error("Form validation failed: %s", cart_form.errors)
    return redirect('cart:cart_detail_view')


def remove_product_from_the_cart(request, product_id):
    cart = Cart(request)
    products = Product.objects.filter(is_featured=False)
    product = get_object_or_404(products, id=product_id)
    cart.remove_from_the_cart(product)
    return redirect(request.META.get('HTTP_REFERER'))


def clear_the_cart(request):
    cart = Cart(request)
    cart.clear_the_cart()
    #redirect the user to the previous page.
    return redirect(request.META.get('HTTP_REFERER'))