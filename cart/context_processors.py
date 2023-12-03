from .cart import Cart
from products.models import Discount, Product

def shopping_cart(request):
    cart = Cart(request)
    data = {'cart': cart}
    return data