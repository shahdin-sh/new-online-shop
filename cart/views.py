import logging
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext as _
from cart.cart import Cart
from cart.decorators import item_in_cart_required
from cart.forms import AddToCartForm
from products.forms import DiscountForm
from products.models import Discount
from products.models import Product

# const values for breadcrumb data
breadcrumb_cart = _('cart')

logger = logging.getLogger(__name__)

@item_in_cart_required
def cart_detail_view(request):
    cart = Cart(request)

    breadcrumb_data = [{'lable': breadcrumb_cart, 'title': breadcrumb_cart}]


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
    add_to_cart_form = AddToCartForm(request.POST, product_stock=product.quantity)

    if add_to_cart_form.is_valid():
        # getting product variant from input that fill by the user
        cleaned_data = add_to_cart_form.cleaned_data

        quantity = cleaned_data.get('quantity', 1)
        size = cleaned_data.get('size')
        color = cleaned_data.get('color')

        cart.add_to_cart(product, size=size, color=color, quantity=quantity)
        return redirect('cart:cart_detail_view')
    else:
        # Log form errors
        logger.error("Form validation failed: %s", add_to_cart_form.errors)

        # creating an error response
        error_message = f"Form validation failed: {add_to_cart_form.errors}"
        response = HttpResponseBadRequest(error_message)
        return response


def remove_product_from_the_cart(request, product_id):
    cart = Cart(request)
    products = Product.objects.all()
    product = get_object_or_404(products, id=product_id)

    cart.remove_from_the_cart(product)

    messages.success(request, f'{product.name} product deleted from your cart successfully.')
 
    return redirect(request.META.get('HTTP_REFERER'))


def clear_the_cart(request):
    cart = Cart(request)

    cart.clear_the_cart()

    messages.success(request, 'your cart deleted successfully')

    #redirect the user to the previous page.
    return redirect(request.META.get('HTTP_REFERER'))


def apply_discount_for_cart_items(request):
    cart = Cart(request)

    discount_form = DiscountForm(request.POST)

    if discount_form.is_valid():
        entered_promo_code = discount_form.cleaned_data.get('promo_code')
        discount_obj = get_object_or_404(Discount ,promo_code=entered_promo_code, status='AC')
        target_products = Product.objects.filter(id__in=request.session['cart'].keys(), discounts=discount_obj)
        unapplied_discounted_product = []
        applied_discounted_product = []
        str_discount_obj_id = str(discount_obj.id)

        if target_products.exists() and not discount_obj.usage_by.filter(id=request.user.id).exists():
            # Retrieve user discounts from session or initialize it
            user_discounts = request.session.get('user_discounts', {})
        
            if f'discount_{str_discount_obj_id}' not in user_discounts:
                user_discounts[f'discount_{str_discount_obj_id}'] = {
                    'id': discount_obj.id,
                    'promo_code' : discount_obj.promo_code,
                    'products': {},
                }


            for product in target_products:
                str_product_id = str(product.id)

                # adding discount to a product for the first time
                if str_product_id not in user_discounts[f'discount_{str_discount_obj_id}']['products']:
                    user_discounts[f'discount_{str_discount_obj_id}']['products'][str_product_id] = product.name

                    unapplied_discounted_product.append(product.name)

                    # applied discount
                    cart.applied_discount(discount_obj, product)
                else:
                    applied_discounted_product.append(product.name)

            # Update the session with the modified 'user_discounts'
            request.session['user_discounts'] = user_discounts
            request.session.modified = True

            # Give feedback to user if discount applied to targeted product or not 
            if unapplied_discounted_product:
                messages.success(request, f"{discount_obj.promo_code} applied for {','.join(unapplied_discounted_product)} successfully.")
                return redirect(request.META.get('HTTP_REFERER'))
        
            elif applied_discounted_product:
                messages.error(request, f"Error: {discount_obj.promo_code} has been applied for {','.join(applied_discounted_product)} before.")
                return redirect(request.Meta.get('HTTP_REFERER'))
            
        else:
            messages.error(request, f'{discount_obj.promo_code} discount is not match to any items in the cart.')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        # Log form errors
        logger.error("Form validation failed: %s", discount_form.errors)

        # creating an error response
        error_message = f"Form validation failed: {discount_form.errors}"
        response = HttpResponseBadRequest(error_message)
        return response
