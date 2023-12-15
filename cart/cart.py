
from products.models import Product

class Cart:
    def __init__(self, request):

        self.request = request
        self.session = request.session

        # check if user has already had cart or not.
        cart = self.session.get('cart')

        if not cart:
            # we create cart key and an empty dictionay for it's value ------> session = {
                # 'cart' = {}
            # }
            cart = self.session['cart'] = {}

        # set cart in the user session.
        self.cart = cart
    
    def save(self):
        self.session.modified = True
    
    def clear_the_cart(self):
        del self.session['cart']
        self.save()
    
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product_obj'] = product
            
        # defining total price and current product stock for each item in cart.
        for item in cart.values():
            item['total_price'] = item['quantity'] * item['product_obj'].price
            item['current_product_stock'] = item['product_obj'].quantity - item['quantity']
            yield item
            
    def add_to_cart(self, product, size='LARGE', color='BLACK', quantity=1):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': quantity,
                'size': size,
                'color': color,
            }
            
        self.cart[product_id]['quantity'] = quantity
        # save changes in the session.
        self.save()

    def remove_from_the_cart(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def lenght(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def is_item(self):
        return False if self.cart == {} else True                                                                                      

    def get_total_price(self):

        cart_total_price = sum(item['quantity'] * item['product_obj'].price for item in self.cart.values()) 

        return cart_total_price
    
    def discounted_total_price(self):
        cart_discounted_total_price = sum(item['discounted_price'] for item in self.cart.values())

        return cart_discounted_total_price
