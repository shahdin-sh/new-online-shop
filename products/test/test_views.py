import random
from accounts.models import CustomUserModel
from django.core.paginator import Paginator
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.forms import model_to_dict
from cart.forms import AddToCartForm
from unittest.mock import patch
from ..models import Product, Category, Comment
from ..forms import CommentForm


class TestProductViews(TestCase):

    def setUp(self):

        self.user = CustomUserModel.objects.create(
            username='user_1', 
            password='user123',
            profile_avatar='/media/default_avatar/img_avatar.png',
        )

        self.category_1 = Category.objects.create(
            name = 'random_name',
            slug = 'random-slug',
            is_featured = False,
            description = 'some_random_description',
        )

        self.product_1 = Product.objects.create(
            name = 'random name',
            description = 'some_random_description',
            quantity = random.randint(1, 100),
            price = 10000,
            size = 'medium',
            color = 'red',
            category = self.category_1,
            slug = 'random-slug',
            feature = False,
            activation = True,
        )

        # comment obj for authenticated users
        self.comment_1 = Comment.objects.create(
            content = 'A random comment for comment number 1',
            is_spam = False,
            product = self.product_1,
            author = self.user,
            name = '',
            email = '',
            parent = None,
            session_token = '',
            rating = 'PERFECT',
        )

        # gust commnet
        self.comment_2 = Comment.objects.create(
            content = 'A reply for comment 1',
            is_spam = False,
            product = self.product_1,
            author = None,
            name = 'jhon',
            email = 'jhon@gmail.com',
            parent = None,
            session_token = 'QWER143FACZVFHRU84KMVLP0UHYL7G54',
            rating = 'POOR'
        )

        # set user_wished_product
        self.product_1.user_wished_product.set([self.user])


        self.client = Client()

        # handling products Urls
        self.shop_categories = reverse('products:product_categories')
        self.category_detail_or_products = reverse('products:category_detail', args=[self.category_1.slug])
        self.product_detail = reverse('products:product_detail', args=[self.product_1.slug])
        self.add_to_wishlist = reverse('products:add_to_wishlist', args=[self.product_1.slug])
        self.remove_from_wishlist = reverse('products:remove_from_wishlist', args=[self.product_1.slug])


     # test shop_categories view
          
    def test_shop_categories_view_status_code(self):
        response = self.client.get(self.shop_categories)
        self.assertEqual(response.status_code, 200)

    def test_shop_categories_view_correct_template(self):
        response = self.client.get(self.shop_categories)
        self.assertTemplateUsed(response, 'categories/shop_categories.html')
    
    def test_shop_categories_view_contains_product(self):
        response = self.client.get(self.shop_categories)
        self.assertIn(self.product_1, response.context['products'])
    
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


    # test products_or_category_detail view
        
    def test_category_detail_view_existing_category(self):
        response = self.client.get(self.category_detail_or_products)
        self.assertIn('category', response.context)
        self.assertEqual(response.status_code, 200)
    
    def test_category_detail_view_nonexisting_category(self):
        nonexisting_category = reverse('products:category_detail', args=['nonexisting-category-slug'])
        response = self.client.get(nonexisting_category)
        self.assertNotIn('category', response.context)
        self.assertEqual(response.status_code, 404)

    def test_category_detail_view_correct_template(self):
        response = self.client.get(self.category_detail_or_products)
        self.assertTemplateUsed(response, 'categories/category_detail.html')

    def test_category_detail_view_contains_cateogry(self):
        response = self.client.get(self.category_detail_or_products)
        self.assertIn('category', response.context)

    def test_category_detail_view_contains_breadcrumb(self):
        response = self.client.get(self.category_detail_or_products)
        self.assertIn('breadcrumb_data', response.context) 

        self.assertEqual(response.context['breadcrumb_data'], [{'lable':f'{self.category_1.name}', 'title': f'{self.category_1.name}', 'middle_lable': 'store', 'middle_url':'products:product_categories'}])


    def test_category_detail_view_contains_product(self):
       response = self.client.get(self.category_detail_or_products)
       self.assertContains(response, self.product_1)


    # test product detail view

    def test_product_detail_view_post_comment_for_authenticated_users(self):
        # log in the user
        self.client.login(username=self.user.username, password=self.user.password)

        # form data for a user comment
        form_data = {
            'content': self.comment_1.content,
            'author': self.comment_1.author,
        }

        # make a post request to post a comment
        response = self.client.post(self.product_detail, form_data)
        self.assertEqual(response.status_code, 302)

    def test_product_detail_view_post_comment_for_guests(self):
        # making sure that the user is logging out
        self.client.login(username=self.user.username, password=self.user.password)
        self.client.logout()

        form_data = {
            'content': self.comment_2.content,
            'name': self.comment_2.name,
            'email': self.comment_2.email,
        }

        response = self.client.post(self.product_detail, form_data)
        self.assertEqual(response.status_code, 302)

    def test_product_detail_view_existing_product(self):
        response = self.client.get(self.product_detail)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'product_detail')

    def test_product_detail_view_nonexisting_product(self):
        response = self.client.get(reverse('products:product_detail', args=['nonexisting-product-slug']))
        self.assertEqual(response.status_code, 404)
      
    def test_product_detail_view_correct_template(self):
        response = self.client.get(self.product_detail)
        self.assertTemplateUsed(response, 'products/product_detail_view.html')
    
    def test_product_detial_view_empty_comment_data(self):
        empty_form_data = {
            'content': ''
        }
        response = self.client.post(self.product_detail, empty_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, [self.comment_1, self.comment_2])
    
    def test_product_detail_view_contains_comment(self):
        response =  self.client.get(self.product_detail)
        self.assertIn('comments', response.context)
    
    def test_product_detail_view_contains_add_to_cart_form(self):
        response =  self.client.get(self.product_detail)
        self.assertIn('add_to_cart_form', response.context)

    def test_product_detail_view_contains_comment_form(self):
        response = self.client.get(self.product_detail)
        self.assertIn('comment_form', response.context)
    
    def test_product_detail_view_breadcrumb_data(self):
        response =  self.client.get(self.product_detail)
        self.assertIn('breadcrumb_data', response.context)
        self.assertEqual(response.context['breadcrumb_data'],  [{'lable':f'{self.product_1.name}', 'title': f'{self.product_1.name}', 'middle_lable': f'{self.product_1.category.name}', 'middle_url': 'products:category_detail', 'middle_url_args': self.product_1.category.slug}])
    
    def test_product_detail_view_logg_form_errors(self):

        with patch('products.views.logger', autospec=True) as mock_logger:

            # invalid_data 
            invalid_data = {
                'content': '',
            }

            # Make a POST request to trigger the form validation error
            response = self.client.post(self.product_detail, invalid_data)

            # if the respone status is 200, indicating that the form submission was unsuccessful
            self.assertEqual(response.status_code, 200)

             # Assert that the logger's error method was called with the expected log message
            mock_logger.error.assert_called_once_with("Form validation failed: %s", {'content': ['This field is required.']})
    
    def test_product_detail_view_comment_spam_status(self):
        response = self.client.get(self.product_detail)
    
        self.assertIn("<input name='website' value='please leave this field blank.' type='hidden'>", response.content.decode('utf-8'))

        self.assertFalse(self.comment_1.is_spam)
        self.assertFalse(self.comment_2.is_spam)
        

        # for comment in [self.comment_1, self.comment_2]:
        #     self.assertEqual(comment.is_spam, False)
    

    def test_product_datail_view_comment_ceration(self):
        test_comment_data = Comment.objects.create(
            content = 'test comment',
                is_spam = False,
                product = self.product_1,
                author = self.user,
                name = '',
                email = '',
                parent = None,
                session_token = '',
                rating = 'POOR'
        )

        # Check that the comment is saved in the database
        self.assertTrue(Comment.objects.filter(content=test_comment_data.content))

    def test_product_detail_view_reply_creation(self):
        parent_comment = self.comment_1
        reply = Comment.objects.create(
            content = 'Reply',
                is_spam = False,
                product = self.product_1,
                author = self.user,
                name = '',
                email = '',
                parent = parent_comment,
                session_token = '',
                rating = 'POOR'
        )

        # Check that the reply is saved  in database
        self.assertTrue(Comment.objects.filter(content=reply.content, parent=parent_comment))
    
    