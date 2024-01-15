from accounts.models import CustomUserModel
from ..models import Product, Category
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from products.views import shop_categories
import random


class TestProductViews(TestCase):

    def setUp(self):

        self.user = CustomUserModel.objects.create(
            username='user_1', 
            profile_avatar='/media/default_avatar/img_avatar.png',
        )

        self.category = Category.objects.create(
            name = 'random_name',
            slug = 'random-slug',
            is_featured = False,
            description = 'some_random_description',
        )

        self.product = Product.objects.create(
            name = 'random name',
            description = 'some_random_description',
            quantity = random.randint(1, 100),
            price = 10000,
            size = 'medium',
            color = 'red',
            category = self.category,
            slug = 'random-slug',
            feature = False,
            activation = True,
        )

        # set user_wished_product
        self.product.user_wished_product.set([self.user])


        self.client = Client()

        # handling products Urls
        self.shop_categories = reverse('products:product_categories')
        self.category_detail_or_products = reverse('products:category_detail', args=[self.category.slug])
        self.product_detail = reverse('products:product_detail', args=[self.product.slug])
        self.add_to_wishlist = reverse('products:add_to_wishlist', args=[self.product.slug])
        self.remove_from_wishlist = reverse('products:remove_from_wishlist', args=[self.product.slug])

       
    def test_shop_categories_response_code(self):
        response = self.client.get(self.shop_categories)
        self.assertEqual(response.status_code, 200)































    # def test_home_page_view_GET_request_and_template_used(self):
    #     response = self.client.get(self.home_page)
    #     print(response)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'home.html')
    
    # def test_shop_categories_view_GET_request_and_template_used(self):
    #     response = self.client.get(self.shop_categories)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'category/shop_categories.html')
    
    # def test_product_detail_view_GET_request_and_template_used(self):
    #     response = self.client.get(self.category_detail_or_products)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'category/category_detail.html')

    # def test_product_detail_view_POST_request(self):
    #     response = self.client.post(self.product_detail)
    #     print(response)
    #     self.assertEqual(response.status_code, 302)








        