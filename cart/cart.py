from django.contrib import messages
from products.models import Product, Discount
from copy import deepcopy

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
    
    def clear_the_cart(self):
        # delete user discount session if it exists, then clear the cart
        user_discounts = self.session.get('user_discounts')

        if user_discounts:
            del self.session['user_discounts']
       
        del self.session['cart']
        self.save()
    
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.select_related('category').filter(id__in=product_ids)

        cart = deepcopy(self.cart)

        for product in products:
            cart[str(product.id)]['product_obj'] = product
    
        # defining total price, discounted total price and current product stock for each item in cart.
        for item in cart.values():

            item['current_product_stock'] = item['product_obj'].quantity - item['quantity']
            item['total_price'] = item['product_obj'].price * item['quantity']

            # create total_discounted_price for items that discount applied for them
            if item.get('discounted_price'):
                item['total_discounted_price'] = item['discounted_price'] * item['quantity']
            yield item

    
    def applied_discount(self, discount_obj, product):
        # Calculate discount process
        if discount_obj.type == Discount.PERCENTAGE_DISCOUNT:
            discounted_price = product.price - ((discount_obj.percent * product.price ) / 100)
        
        elif discount_obj.type == Discount.FIXED_AMOUNT_DISCOUNT:
            discounted_price = product.price - discount_obj.value
        
        # discounted_price should be netural
        discounted_price = int(str(discounted_price)[:-3] + '000')
        
        # save discounted_price in cart
        self.cart[str(product.id)]['discounted_price'] = discounted_price

        self.save()
    
    def remove_from_the_cart(self, product):
        product_id = str(product.id)

        user_discounts = self.session.get('user_discounts')

        if user_discounts:
            keys_to_delete = []
            for key, value in user_discounts.items():
                if product_id in value.get('products', {}):
                    del value['products'][product_id]

                    # If there are no more products under this discount, mark it for deletion
                    if value['products'] == {}:
                        keys_to_delete.append(key)

            # delete discount_ids that there have no products
            for key in keys_to_delete:
                del user_discounts[key]

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def lenght(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def is_item(self):
        return False if self.cart == {} else True    

    def is_discount_applies(self, product):
        is_discount = False

        for item in self:
            if item.get('discounted_price') and item['product_obj'].id == product.id:
                is_discount = True
        return is_discount
    
    def get_total_price(self):
        return sum(item['total_price'] for item in self) 

    def get_total_discounted_price(self):
        # Temporary storage for calculation
        temporary_items = []

        for item in self:
            # Create a shallow copy of each item for temporary manipulation
            copied_item = item.copy()

            # items that discount applied to them
            if copied_item.get('total_discounted_price'):
                copied_item['total_price'] = 0
            
            # Add the temporarily modified item to the list
            temporary_items.append(copied_item)
        

        items_total_price = sum(item['total_price'] for item in temporary_items)

        # total price  of items that are calculation with their discounted_prices were set to zero
        items_total_discounted_price = sum(item.get('total_discounted_price', 0) for item in temporary_items)

        return items_total_price + items_total_discounted_price
