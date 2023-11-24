from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponse
from .cart import Cart
from .decorators import item_in_cart_required
from .forms import AddToCartForm
from products.models import Product
import logging
from products.forms import DiscountForm
from products.models import Discount
from django.contrib import messages

@item_in_cart_required
def cart_detail_view(request):
    cart = Cart(request)

    breadcrumb_data = [{'lable':'cart', 'title': 'Cart'}]
    
    context = {
        'cart': cart,
        'breadcrumb_data': breadcrumb_data,
    }

    return render(request, 'cart_detail_view.html', context)


# we use this view as action of our forms in 'cart_detail_view' and 'product_detail_view'
def add_product_to_the_cart(request, product_id):
    cart = Cart(request)
    products = Product.objects.all()
    product = get_object_or_404(products, id=product_id)
    cart_form = AddToCartForm(request.POST, product_stock=product.quantity)
    if cart_form.is_valid():
        # getting product variant from input that fill by the user
        cleaned_data = cart_form.cleaned_data
        quantity = cleaned_data.get('quantity', 1)
        size = cleaned_data.get('size')
        color = cleaned_data.get('color')
        cart.add_to_cart(product, size=size, color=color, quantity=quantity)
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


def apply_discount_for_cart_items(request):
    cart = Cart(request)
    cart_items_ids = request.session['cart'].keys()
    discount_form = DiscountForm(request.POST)
    if discount_form.is_valid():
        cleaned_data = discount_form.cleaned_data
        entered_promo_code = cleaned_data.get('promo_code')
        # all the promo codes are unique and each promo code should not be expired.
        discount_obj = get_object_or_404(Discount.objects.filter(promo_code=entered_promo_code, status='AC'))
        # check if discount obj is applied for each item in cart_items
        cart_items_with_discount = Product.objects.filter(id__in=cart_items_ids, discounts=discount_obj)
        if not discount_obj.check_and_delete_if_expired():
            if cart_items_with_discount.exists():
                discounted_price = cart.applying_discount(discount_obj.value, discount_obj.percent, discount_obj.type)
                # no solution has been found yet.
                print(discounted_price)
                # change the discount status to deactive it means that each discount after use are not usable anymore.
                discount_obj.status = 'DC'
                discount_obj.save()
                messages.success(request, 'your discount applied successfully.')
                # redirect to the current page.
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                return HttpResponse('The discount code that you have entered is not valid')
        else:
            return HttpResponse('Your discount has been expired.')
    else:
        # Log form errors
        logger = logging.getLogger(__name__)
        logger.error("Form validation failed: %s", discount_form.errors)