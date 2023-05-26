

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

