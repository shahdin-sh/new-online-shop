from accounts.models import CustomUserModel
from ..cart import Cart
from products.models import Product, Category
from django.test import TestCase, Client
from django.urls import reverse


class TestProductViews(TestCase):

    def setUp(self):
        self.user = CustomUserModel.objects.create(
            username='user_1', 
            profile_avatar='/media/default_avatar/img_avatar.png',
        )
        self.category = Category.objects.create(
        name = 'some_random_name',
        slug = 'some_random_slug',
        is_featured = False,
        parent = None,
        description = 'some_random_description',
        )
        self.product = Product.objects.create(
            name = 'some_random_name',
            slug = 'some_random_slug',
            description = 'some_random_description',
            quantity = 3,
            is_featured = False,
            price = 10000,
            size = 'medium',
            color = 'red',
            quality = 'good',
            category = self.category,
        )
        # self.shopping_cart = Cart.objects.create(
        #     quantity= '5',
        #     product_obj= self.product,
        # )
        self.client = Client()
        # handling products Urls
        self.cart_detail_view = reverse('cart:cart_detail_view')
    
    # checkout why AssertionError: 404 != 200


    def test_cart_detail_view_GET_request_and_template_used(self):
        response = self.client.get(self.cart_detail_view)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart_detail_view.html')
    
   