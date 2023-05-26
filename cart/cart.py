

class Cart:
    def __init__(self, request):

        self.request = request
        self.session = request.session

        # check if user has already had cart or not
        cart = self.session.get['cart']

        if not cart:
            # we create cart key and an empty dictionay for it's value ------> session = {
                # 'cart' = {}
            # }
            cart = self.session['cart'] = {}

        # when we determine our cart value we set it up in our init method:
        self.cart = cart
    
    def save(self):
        self.session.modified = True


    def add_to_cart(self, product, quantity=1):
        product_id = str(product)

        # check if this product have been added to user cart or not
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': quantity
            }
            # session = {
            #   'cart' = {
                    # product_id = {
                        # quantity = 1
                    # }
        #       }
            # }
        # if we already had our product in the cart then user wants to add more quantity of the current product.
        else:
            self.cart[product_id]['quantity'] += quantity
        # save changes in the session 
        self.save()
    
    def remove_from_the_cart(self, product):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
            


