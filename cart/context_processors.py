from .cart import Cart

def shopping_cart(request):
    data = {
        'cart' : Cart(request),
    }
    return data
