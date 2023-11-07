from .cart import Cart
from products.models import Discount, Product

def shopping_cart(request):
    data = {
        'cart' : Cart(request),
    }
    return data