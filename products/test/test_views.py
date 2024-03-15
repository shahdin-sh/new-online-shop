import random
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.core.paginator import Paginator
from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import CustomUserModel
from products.models import Product, Category, Comment, Discount
from unittest.mock import patch
from cart.cart import Cart


class TestProductsViews(TestCase):

    def setUp(self):

        self.user = CustomUserModel.objects.create(
            username = 'user',
            email = 'User123$@gmail.com',
            password = 'USER123@',
            profile_avatar = '/media/default_avatar/img_avatar.png',
            first_name = 'user first name', 
            last_name = 'user last name',
            date_joined = '2024-01-26 12:10:54.566470+00:00'
        )

        self.user_2 = CustomUserModel.objects.create(
            username = 'user2',
            email = 'User2123$@gmail.com',
            password = 'USER2123@',
            profile_avatar = '/media/default_avatar/img_avatar.png',
            first_name = 'user first name 2', 
            last_name = 'user last name 2',
            date_joined = '2024-01-27 12:10:54.566470+00:00'
        )

        self.category_1 = Category.objects.create(
            name = 'random_name',
            slug = 'random-slug',
            is_featured = False,
            description = 'some_random_description',
        )

        # A Percentage Discount
        self.percentage_discount = Discount.objects.create(
            type = Discount.PERCENTAGE_DISCOUNT,
            value = None,
            percent = 23.4,
            description = '10 percent off discount',
            status = Discount.ACTIVE,
            # expiration date
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

        # create a sample request object
        class Request:
            def __init__(self):
                self.session = {}

        self.request = Request()

        self.client = Client()

        # handling products Urls
        self.shop_categories = reverse('products:product_categories')
        self.category_detail_or_products = reverse('products:category_detail', args=[self.category_1.slug])
        self.product_detail = reverse('products:product_detail', args=[self.product_1.slug])
        self.add_to_wishlist = reverse('products:add_to_wishlist', args=[self.product_1.slug])
        self.remove_from_wishlist = reverse('products:remove_from_wishlist', args=[self.product_1.slug])
        self.wishlist_view = reverse('account:wishlist_view')

        # handling nonexisting products Urls
        self.nonexisting_category = reverse('products:category_detail', args=['nonexisting-category-slug'])
        self.nonexisting_product = reverse('products:product_detail', args=['nonexisting-product-slug'])


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
        response = self.client.get(self.nonexisting_category)
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


    # test product_detail view

    def test_product_detail_view_post_comment_for_authenticated_users(self):
        # log in the user
        self.client.force_login(self.user)

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
        self.client.force_login(self.user)
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
        response = self.client.get(self.nonexisting_product)
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
    
    def test_product_detail_contains_has_discount_boolean(self):
        response = self.client.get(self.product_detail)
        self.assertIn('product_detail_has_discount', response.context)
    
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
    
        self.assertIn("<input name='website' value='please leave this field blank' type='hidden'>", response.content.decode('utf-8'))

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
    
    def test_product_detail_view_redirect_page(self):
        data = {
            'content': 'random content'
        }

        response = self.client.post(self.product_detail, data)
        self.assertRedirects(response, self.product_detail, status_code=302, target_status_code=200)
    
    # adding this test at 3/9/2024
    def test_product_detail_discounted_price(self):
        pass
        # # setup cart data
        # cart = Cart(self.request)

        # # adding item to the cart
        # cart.add_to_cart(self.product_1, self.product_1.size, self.product_1.color, quantity=4)

        # # applying discount to the cart item
        # cart.applied_discount(self.percentage_discount, self.product_1)

        # # set discounted price for product detail
        # discounted_price = self.cart[str(self.product_1.id)].get('discounted_price')
        # self.product_1.discounted_price = discounted_price

        # self.assertEqual(self.product_1.discounted_price, discounted_price)
        # self.assertNotEqual(self.product_1.discounted_price, 0)
    


    # test add_to_wishlist view
    
    def test_add_to_wishlist_view_access_for_authenticated_users(self):
        self.client.force_login(self.user)

        response = self.client.get(self.add_to_wishlist)
        self.assertEqual(response.status_code, 200)
       
    def test_add_to_wishlist_view_denied_access_for_anonymous_users(self):

        # log out the user
        self.client.force_login(self.user)
        self.client.logout()
        
        response = self.client.get(self.add_to_wishlist)

        # Check anonymous user is redirected to login page
        self.assertRedirects(response, f'/accounts/login/?next=/products/{self.product_1.slug}/add_to_wishlist', status_code=302, target_status_code=200)
    
    def test_add_to_wishlist_view_nonexisting_product(self):
        self.client.force_login(self.user)

        response = self.client.get(self.nonexisting_product)
        self.assertEqual(response.status_code, 404)
    
    def test_add_to_wishlist_view_add_if_user_not_in_user_wished_product(self):
        self.client.force_login(self.user_2)

        response = self.client.get(self.add_to_wishlist)

        # test the success message
        messages = [str(message) for message in list(get_messages(response.wsgi_request))]
        self.assertEqual(len(messages), 1)
        self.assertIn(f'{self.product_1.name} add to your wishlist successfuly.', messages)

        # user_2 is not in product_1.user_wished_product and based on view logic user_2 add to wished_product and redirection will happen, 302 status code
        self.assertRedirects(response, self.wishlist_view, status_code=302, target_status_code=200)


    def test_add_to_wishlist_view_dont_add_if_user_in_user_wished_product(self):
        self.client.force_login(self.user)

        response = self.client.get(self.add_to_wishlist)

        # user is already in product_1 wished product and base on view logic the response status code is 200
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'this product has already added to your wishlist.')



    # test remove from wishlist view
    
    def test_remove_from_wishist_view_accsess_for_authenticated_users(self):
        self.client.force_login(self.user_2)

        response = self.client.get(self.remove_from_wishlist)
        self.assertEqual(response.status_code, 200)
    
    def test_remove_from_wishlist_view_denied_access_for_anonymous_users(self):
        # log out the user
        self.client.force_login(self.user)
        self.client.logout()

        response = self.client.get(self.remove_from_wishlist)

        # login required decoator cause redirection to login page for anonymous users
        self.assertRedirects(response,  f'/accounts/login/?next=/products/{self.product_1.slug}/remove_from_wishlist', status_code=302, target_status_code=200)
    
    def test_remove_from_wishist_view_nonexisting_product(self):
        self.client.force_login(self.user)

        response = self.client.get(self.nonexisting_product)
        self.assertEqual(response.status_code, 404)

    def test_remove_from_wishlist_view_remove_if_user_in_user_wished_product(self):
        self.client.force_login(self.user)

        # if user is in user wished product then Remove user
        self.assertTrue(self.user in self.product_1.user_wished_product.all())

        response = self.client.get(self.remove_from_wishlist)

        self.product_1.user_wished_product.remove(self.user)

        self.assertTrue(self.user not in self.product_1.user_wished_product.all())

        self.assertRedirects(response, self.wishlist_view, status_code=302, target_status_code=200)
    
    def test_remove_from_wishist_view_dont_remove_if_user_is_not_in_user_wished_product(self):
        self.client.force_login(self.user_2)

        self.assertNotIn(self.user_2, self.product_1.user_wished_product.all())

        response = self.client.get(self.remove_from_wishlist)

        self.assertEqual(response.status_code, 200)
        