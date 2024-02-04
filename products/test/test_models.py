from django.contrib.auth import get_user_model
from django.db import DataError
from django.test import TestCase, Client
from django.urls import reverse
from products.models import Product, Category, Discount, Comment



class TestProductsModels(TestCase):
    
    def setUp(self):
         
        self.user = get_user_model().objects.create(
            username = 'user',
            email = 'User123$@gmail.com',
            password = 'USER123@',
            profile_avatar = '/media/default_avatar/img_avatar.png',
            first_name = 'user first name', 
            last_name = 'user last name',
            date_joined = '2024-01-26 12:10:54.566470+00:00'
        )


        self.category = Category.objects.create(
            name = 'Category 1',
            slug = 'category-1',
            is_featured = False,
            description = 'Description for category 1',
        )

        # A Percentage Discount
        self.percentage_discount = Discount.objects.create(
            promo_code = 'ABCD',
            type = Discount.PERCENTAGE_DISCOUNT,
            value = None,
            percent = 10.0,
            description = '10 percent off discount',
            expiration_date = '2024-12-31T23:59:59',
            status = Discount.ACTIVE
        )

        # A Fixed Amount Discount
        self.fixed_amount_discount = Discount.objects.create(
            promo_code = 'EFGH',
            type = Discount.FIXED_AMOUNT_DISCOUNT,
            value = 50000,
            percent = None,
            description = 'A value based discount',
            expiration_date = '2024-12-31T23:59:59',
            status = Discount.ACTIVE
        )

        self.product = Product.objects.create(
            name = 'test product',
            description = 'text for test product',
            quantity = 10,
            price = 100000,
            slug = 'test-product',
            size = Product.SIZE_CHOICES[0],
            color = Product.COLOR_CHOICES[0],
            image = 'media\product\bn1-2-1420x945.webp',
            banner = 'media\product_banners\bn-hf-1-570x340.jpg',
            datetime_created = '2023-12-03 17:17:59.102689+00:00',
            datetime_modified = '2024-01-28 13:47:27.943519+00:00',
            category = self.category,
            activation = True,
            feature = False
        )

        # if a author field (authenticated user) is filled then name,email and session_token fields should remain null
        self.authorized_comment = Comment.objects.create(
            content = 'This is a comment for perfect product',
            is_spam = False,
            product = self.product,
            author = self.user,
            name= '',
            email= '',
            parent=None,
            session_token='',
            rating=Comment.RATING_CHOICES[4]
        )

        # if name,email and session_token (guest information) fields are filled then author field should remain null 
        self.guest_comment = Comment.objects.create(
            content = 'This is a comment for perfect product',
            is_spam = False,
            product = self.product,
            author = None,
            name = 'Jane Smith',
            email = 'jane@example.com',
            parent = None,
            session_token = 'qwertyuioplkjhgfdsazxcvb12345678',
            rating = 'PERFECT'
        )
        # Many to Many products fields
        self.product.user_wished_product.set([self.user])
        self.product.discounts.set([self.percentage_discount, self.fixed_amount_discount])

        # selected product field for category
        self.category.selected_product = self.product
        self.category.save()

        self.client = Client()


    # Test Category model
      

    # CRUD Testing
        
    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Category 1')
        self.assertEqual(self.category.slug, 'category-1')
        self.assertFalse(self.category.is_featured)
        self.assertEqual(self.category.description, 'Description for category 1')
    
    def test_category_update(self):
        self.category.description = 'A new description for category'
        self.category.save()
        
        self.assertEqual(self.category.description, 'A new description for category')
    
    def test_category_deletion(self):

       # Delete Product models when deleting associated Category objects due to Protected on_delete attribute.
        self.product.delete()

        self.category.delete()

        # check if category object delete
        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(name='Category 1')
    

    # Field attributes Testing
            
    def test_category_max_lenght_validation(self):
        with self.assertRaises(DataError):
            # max_lenght is 200 for name field
            self.category.name = 'A' * 201
            self.category.save()
    
    def test_cateogry_fields_attributes(self):
        self.assertEqual(self.category.is_featured, False)

        # description is a blankable field
        self.assertEqual(self.category.description, 'Description for category 1')

        self.category.description = ''
        self.category.save()

        self.assertEqual(self.category.description, '')

        # is_featured is a nullable field
        self.category.is_featured = None
        self.category.save()
        self.assertIsNone(self.category.is_featured)
    

    # Relationships Testing

    def test_category_related_models_or_objects(self):
        self.assertEqual(self.category.selected_product, self.product)


    def test_category_selected_product_field_SET_NULL_after_deletion(self): 
        # delete the selected prodcut
        self.product.delete()

        # Fetch the category again from the database
        self.category.refresh_from_db()

        # Based on on_delete method selected_product field after the deletion of related product should remain to null
        self.assertIsNone(self.category.selected_product)

    def test_category_realtions_with_models(self):
        self.assertEqual(self.category.selected_product, self.product)

    def test_category_reverse_access_related_models_objects(self):
        with self.assertRaises(AttributeError):
            self.category.selected_product_set.all()
    

    # Custom method Testing

    def test_category_str_method(self):
        self.assertEqual(self.category.__str__(), self.category.name)
    
    def test_category_get_absolute_url_method(self):
        category_url = reverse('products:category_detail', args=[self.category.slug])
        self.assertEqual(self.category.get_absolute_url(), category_url)

        


      