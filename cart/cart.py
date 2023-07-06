from typing import Any
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
    
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product_obj'] = product
        
        for item in cart.values():
            yield item

            
    def add_to_cart(self, product, quantity=1):
        product_id = str(product.id)

        # check if this product have been added to user cart or not.
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': quantity
            }
            # session = {
            #   'cart' = {
                    # product_id = {
                        # quantity: 1,
                    # }
        #       }
            # }
        # if we already had our product in the cart then user wants to add more quantity of the current product.
        else:
            self.cart[product_id]['quantity'] += quantity
        # save changes in the session.
        self.save()

    def remove_from_the_cart(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def __len__(self):
        return len(self.cart.keys())
    
    def clear_the_cart(self):
        del self.session['cart']
        self.save()
    
    def total_price(self):
        for i in self.cart.values():
            # our values in the each product is 'quantity' and 'product_objs', i[product_obj].price is product.price.
            return sum(i['quantity'] * i['product_obj'].price)