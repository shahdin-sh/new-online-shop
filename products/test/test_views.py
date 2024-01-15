import random
from ..views import shop_categories
from accounts.models import CustomUserModel
from django.core.paginator import Paginator
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from products.views import shop_categories
from ..models import Product, Category


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


     # test shop_categories_view
          
    def test_shop_categories_view_status_code(self):
        response = self.client.get(self.shop_categories)
        self.assertEqual(response.status_code, 200)

    def test_shop_categories_view_correct_template(self):
        response = self.client.get(self.shop_categories)
        self.assertTemplateUsed(response, 'categories/shop_categories.html')
    
    def test_shop_categories_view_contains_product(self):
        response = self.client.get(self.shop_categories)
        self.assertIn(self.product, response.context['products'])
    
    def test_shop_categories_view_pagination(self):
        # test if pagination is working correctly
        response = self.client.get(self.shop_categories)
        paginator = Paginator(response.context['products'], 9)

        self.assertEqual(paginator.num_pages, 1) # Assuming there are fewer than 9 products in the test setup
    
    def test_shop_categories_view_contains_page_range(self):
        response = self.client.get(self.shop_categories)
        self.assertIn('page_range', response.context)

        # Check if 'page_range' is iterable and not empty
        page_range = response.context['page_range']
    
    
        for products_page_number in page_range:
            self.assertInHTML(f"<li class='active'><a href='?page={products_page_number}'>{products_page_number}</a></li>", response.content.decode('utf-8'))
    
    def test_shop_categories_view_contains_breadcrumb(self):
        response = self.client.get(self.shop_categories)
        self.assertIn('breadcrumb_data', response.context)
        self.assertEqual(response.context['breadcrumb_data'],  [{'lable':'store', 'title': 'Store'}])







        