import string
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import DataError as django_db_dataerror, models
from django.db.models.deletion import ProtectedError
from django.db.utils import IntegrityError
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
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
            type = Discount.PERCENTAGE_DISCOUNT,
            value = None,
            percent = 23.4,
            description = '10 percent off discount',
            status = Discount.ACTIVE,
            # expiration date
        )

        # A Fixed Amount Discount
        self.fixed_amount_discount = Discount.objects.create(
            type = Discount.FIXED_AMOUNT_DISCOUNT,
            value = 50000,
            percent = None,
            description = 'A value based discount',
            status = Discount.ACTIVE,
            # expiration_date
        )

        self.product = Product.objects.create(
            name = 'test product',
            description = 'text for test product',
            quantity = 10,
            price = 100000,
            slug = 'test-product',
            size = Product.SIZE_CHOICES[0],
            color = Product.COLOR_CHOICES[0],
            image = 'product/bn1-2-1420x945.webp',
            banner = 'product_banners/bn-hf-1-570x340.jpg',
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
    

    # Field Attributes Testing
            
    def test_category_max_lenght_validation(self):
        with self.assertRaises(django_db_dataerror):
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
    

    # Custom Methods Testing

    def test_category_str_method(self):
        self.assertEqual(self.category.__str__(), self.category.name)
    
    def test_category_get_absolute_url_method(self):
        category_url = reverse('products:category_detail', args=[self.category.slug])
        self.assertEqual(self.category.get_absolute_url(), category_url)
    


    # Test Discount model
    

    # CRUD Testing
        
    def test_discount_creation(self):
        self.assertEqual(self.percentage_discount.type, Discount.PERCENTAGE_DISCOUNT)
        self.assertEqual(self.percentage_discount.value, None)
        self.assertEqual(self.percentage_discount.percent, 23.4)
        self.assertEqual(self.percentage_discount.description, '10 percent off discount')
        self.assertEqual(self.percentage_discount.status, Discount.ACTIVE)

        # make sure that promo code and expiration date are not none
        self.assertIsNotNone(self.percentage_discount.promo_code)
        self.assertIsNotNone(self.percentage_discount.expiration_date)

        self.assertEqual(self.fixed_amount_discount.type, Discount.FIXED_AMOUNT_DISCOUNT)
        self.assertEqual(self.fixed_amount_discount.value, 50000)
        self.assertEqual(self.fixed_amount_discount.percent, None)
        self.assertEqual(self.fixed_amount_discount.description, 'A value based discount')
        self.assertEqual(self.fixed_amount_discount.status, Discount.ACTIVE)

        # make sure that promo code and expiration date are not none
        self.assertIsNotNone(self.fixed_amount_discount.promo_code)
        self.assertIsNotNone(self.fixed_amount_discount.expiration_date)


    
    def test_discount_update(self):
        self.fixed_amount_discount.status = Discount.DEACTIVE
        self.fixed_amount_discount.save()
        
        self.assertEqual(self.fixed_amount_discount.status, Discount.DEACTIVE)
    
    def test_discount_deletion(self):
        self.percentage_discount.delete()

        # check discount object delete
        with self.assertRaises(Discount.DoesNotExist):
            Discount.objects.get(promo_code=self.percentage_discount.promo_code)
    

    # Field Attributes Testing
            
    def test_discount_fields_max_lenght_validation(self):
        with self.assertRaises(django_db_dataerror):
            # promo code field max lenght
            self.percentage_discount.promo_code = 'A' * 5
            self.percentage_discount.save()

            self.fixed_amount_discount.promo_code = 'A' * 5
            self.fixed_amount_discount.save()

            # type field max lenght
            self.percentage_discount.type = 'A' * 226
            self.percentage_discount.save()

            self.fixed_amount_discount.type = 'A' * 226
            self.fixed_amount_discount.save()

            # percent field max lenght
            self.percentage_discount.percent = '1' * 4
            self.percentage_discount.save()

            # description field max lenght
            self.percentage_discount.description = 'A' * 101
            self.percentage_discount.save()

            self.fixed_amount_discount.description = 'A' * 101
            self.fixed_amount_discount.save()

            # status field max lengt
            self.percentage_discount.status = 'A' * 226
            self.percentage_discount.save()

            self.fixed_amount_discount.status = 'A' * 256
            self.fixed_amount_discount.save()

    def test_discount_promo_code_fields_attributes(self):
        # promo code is a blankable field
        self.percentage_discount.promo_code = ''
        self.percentage_discount.save()


        self.fixed_amount_discount.promo_code = ''
        self.fixed_amount_discount.save()

    def test_disount_type_field_attributes_validation(self):
        # test type choices
        for choice in Discount.DISCOUNT_TYPE_CHOICES:
            self.percentage_discount.type = choice
            self.percentage_discount.save()

            self.assertEqual(self.percentage_discount.type, choice)

            self.fixed_amount_discount.type = choice
            self.fixed_amount_discount.save()

            self.assertEqual(self.fixed_amount_discount.type, choice)
    
    def test_discount_value_field_attributes_validation(self):
        # vlaue field is nullable and blankable field
        self.fixed_amount_discount.value = None
        self.fixed_amount_discount.save()

        self.assertEqual(self.fixed_amount_discount.value, None)
        self.assertIsNone(self.percentage_discount.value)
    
    def test_discount_percent_field_attribute_validation(self):
        # percent field is nullable and blankable field
        self.percentage_discount.percent = None
        self.percentage_discount.save()

        self.assertEqual(self.percentage_discount.percent, None)
        self.assertIsNone(self.fixed_amount_discount.percent)

        # test percnet range, decimal_places = 1, max=100, min=1
        valid_percent_values = [23.2, 78.0, 1.0, 99.9]
        for valid_percent_value in valid_percent_values:
            self.percentage_discount.percent = valid_percent_value
            self.percentage_discount.save()

            self.assertEqual(self.percentage_discount.percent, valid_percent_value)
        
        # invalid_percent_values = [-12, 101, 99.99, 32.32]
        # for invalid_percent_valaue in invalid_percent_values:

        #     self.percentage_discount.percent = invalid_percent_valaue
        #     self.percentage_discount.save() 

    def test_discount_expiration_date_field_attributes_validation(self):
        # test default attribute for expiration_date field
        discount_obj = Discount.objects.create(
            type = Discount.FIXED_AMOUNT_DISCOUNT,
            value = 100000,
            percent = None,
            description = '',
            status = Discount.ACTIVE
        )

        ten_days_from_now = (timezone.now() + timezone.timedelta(days=10)).replace(hour=0,minute=0, second=0, microsecond=0) 
        self.assertEqual(discount_obj.expiration_date.replace(hour=0,minute=0, second=0, microsecond=0), ten_days_from_now)

    def test_discount_status_field_attribute_validation(self):
        # test choices attribute from status field
        for choice in Discount.DISCOUNT_STATUS_CHOICES:
            self.percentage_discount.status = choice
            self.percentage_discount.save()

            self.assertEqual(self.percentage_discount.status, choice)

            self.fixed_amount_discount.status = choice
            self.fixed_amount_discount.save()

            self.assertEqual(self.fixed_amount_discount.status, choice)
        

    # Custom Methods Testing
            
    def test_discount_str_method(self):
        self.assertEqual(self.percentage_discount.__str__(), f'{self.percentage_discount.promo_code} | {self.percentage_discount.description}')

        self.assertEqual(self.fixed_amount_discount.__str__(), f'{self.fixed_amount_discount.promo_code} | {self.fixed_amount_discount.description}')
    
    def test_discount_clean_value_method(self):
        self.assertEqual(self.fixed_amount_discount.clean_value(),  f'{self.fixed_amount_discount.value: ,} T' )
        self.assertIsNone(self.percentage_discount.clean_value())
    
    def test_discount_clena_percent_method(self):
        self.assertEqual(self.percentage_discount.clean_percent(), f'{self.percentage_discount.percent: ,} %')
    
    def test_discount_check_and_delete_if_expired(self):
        earlier_time_than_now =  timezone.now() - timezone.timedelta(days=1)

        self.percentage_discount.expiration_date = earlier_time_than_now
        self.percentage_discount.save()

        self.fixed_amount_discount.expiration_date = earlier_time_than_now
        self.fixed_amount_discount.save()


        self.percentage_discount.check_and_delete_if_expired()

        self.fixed_amount_discount.check_and_delete_if_expired()

        # check discount obj delete
        with self.assertRaises(Discount.DoesNotExist):
            Discount.objects.get(promo_code=self.percentage_discount.promo_code)

            Discount.objects.get(promo_code=self.fixed_amount_discount.promo_code)


    # Test Promo Code Conditions
            
    def test_discount_generating_promo_code_automation_when_object_created(self):
        discount_obj = Discount.objects.create(
            type = Discount.FIXED_AMOUNT_DISCOUNT,
            value = 100000,
            percent = None,
            description = 'random description for discount',
            status = Discount.ACTIVE
        )
        
        # ensure that promo code field is never blank
        self.assertNotEqual(discount_obj.promo_code, '')

        # ensure that promo code is not none and it contains with 4 uppercase letters without any number
        self.assertIsNotNone(discount_obj.promo_code)

        self.assertEqual(len(discount_obj.promo_code), 4)

        self.assertTrue(all(char in string.ascii_letters.upper() for char in discount_obj.promo_code))

        # ensure that after the object is created the promo code is unchangeable
        discount_obj.promo_code = 'ABCD'
        discount_obj.save()

        self.assertNotEqual(discount_obj.promo_code, 'ABCD')
    
    def test_discount_promo_code_manually_creation_status(self):

        with self.assertRaises(Discount.DoesNotExist):
            Discount.objects.create(
                promo_code = 'ABCD',
                type = Discount.FIXED_AMOUNT_DISCOUNT,
                value = 100000,
                description = 'random description for discount',
                status = Discount.ACTIVE
            )


    # Test Custom Validations
            
    def test_discount_expiration_date_clean_method_condition(self):
        discount_obj_with_earlier_ex_date_than_now = Discount.objects.create(
            type = Discount.FIXED_AMOUNT_DISCOUNT,
            value = 100000,
            percent = None,
            description = 'random',
            status = Discount.ACTIVE,
            expiration_date = timezone.now() - timezone.timedelta(minutes=1)
        )

        discount_obj_with_exact_ex_date_than_now = Discount.objects.create(
            type = Discount.FIXED_AMOUNT_DISCOUNT,
            value = 100000,
            percent = None,
            description = 'random',
            status = Discount.ACTIVE,
            expiration_date = timezone.now()
        )

        with self.assertRaises(ValidationError):
            discount_obj_with_earlier_ex_date_than_now.full_clean()
            discount_obj_with_exact_ex_date_than_now.full_clean()

    def test_value_and_percent_field_clean_method_condition(self):
        self.percentage_discount.value = 100000
        self.percentage_discount.save()

        self.fixed_amount_discount.percent = 10.0
        self.fixed_amount_discount.save()

        # one of the value or percent field can be filled
        with self.assertRaises(ValidationError):
            self.percentage_discount.full_clean()
            self.fixed_amount_discount.full_clean()
    
    def test_discount_type_field_relation_to_value_and_percent_field_clean_method_condition(self):
        # percentage discount type is PD
        self.percentage_discount.percent = None
        self.percentage_discount.value = 100000
        self.percentage_discount.save()

        # fixed amount discount type is FAD
        self.fixed_amount_discount.value = None
        self.fixed_amount_discount.percent = 10.0
        self.fixed_amount_discount.save()

        with self.assertRaises(ValidationError):
            self.percentage_discount.full_clean()
            self.fixed_amount_discount.full_clean()


    # Test Product Model
    

    # CRUD Testing
    
    def test_product_creation(self):
        self.assertEqual(self.product.name, 'test product')
        self.assertEqual(self.product.description, 'text for test product')
        self.assertEqual(self.product.quantity, 10)
        self.assertEqual(self.product.price, 100000)
        self.assertEqual(self.product.slug, 'test-product')
        self.assertEqual(self.product.size, Product.SIZE_CHOICES[0])
        self.assertEqual(self.product.color, Product.COLOR_CHOICES[0])
        self.assertEqual(self.product.image, 'product/bn1-2-1420x945.webp')
        self.assertEqual(self.product.banner, 'product_banners/bn-hf-1-570x340.jpg')
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.activation, True)
        self.assertEqual(self.product.feature, False)
    
    def test_product_update(self):
        self.product.name = 'product number 1'
        self.product.save()

        self.assertEqual(self.product.name, 'product number 1')
    
    def test_product_deletion(self):
        self.product.delete()

        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(id=self.product.id)


    # Field Attributes Testing
    
    def test_product_fields_max_lenght_validation(self):
        with self.assertRaises(django_db_dataerror):
            self.product.name = 'A' * 201
            self.product.save()

            self.product.size = 'A' * 201
            self.product.save()

            self.product.color = 'A' * 201
            self.product.save()
    
    def test_product_description_field_attributes_validation(self):
        # description field is a blankable field
        self.product.description = ''
        self.product.save()

        self.assertEqual(self.product.description, '')

        # description field is a nullable field
        self.product.description = None
        self.product.save()

        self.assertIsNone(self.product.description)
    
    def test_product_quantity_field_attributes_validation(self):
        invalid_quantity_range = [101, 200, -1, -11]

        for quantity in invalid_quantity_range:
            self.product.quantity = quantity
            self.product.save()

            with self.assertRaises(ValidationError):
                self.product.full_clean()
    
    def test_product_invalid_price_amount(self):
        invalid_price_amount = [10000001, 0, 999]
        
        for price in invalid_price_amount:
            with self.assertRaises(ValidationError):
                self.product.price = price
                self.product.save()
                
                self.product.full_clean()
    
    def test_product_negative_price_amount(self):
        pass
                
    def test_product_slug_field_being_unique_validation(self):
        
        # the slug belongs to the self.product.slug
        with self.assertRaises(IntegrityError):
            Product.objects.create(
                name = 'product 1', 
                quantity = 1, 
                price = 10000,
                slug = 'test-product',
                category = self.category
            )
    
    def test_product_size_field_attributes_validation(self):
        # test choices attribute
        for choice in Product.SIZE_CHOICES:
            self.product.size = choice
            self.product.save()
            self.assertEqual(self.product.size, choice)

        # test default attribute
        product = Product.objects.create(
            name = 'product', 
            quantity = 1, 
            price = 10000,
            slug = 'product',
            category = self.category
        )

        self.assertEqual(product.size, Product.SIZE_CHOICES[0])

    def test_product_color_field_attributes_validation(self):
        # test choices attribute
        for choice in Product.COLOR_CHOICES:
            self.product.color = choice
            self.product.save()

            self.assertEqual(self.product.color, choice)
        
        # test default attribute
        product = Product.objects.create(
            name = 'product', 
            quantity = 1, 
            price = 10000,
            slug = 'product',
            category = self.category
        )

        self.assertEqual(product.color, Product.COLOR_CHOICES[0])
    
    def test_product_image_field_attributes_validation(self):
        # ensure that the image file uploaded in its correct path
        self.assertTrue(self.product.image.name.startswith('product/'))
        self.assertTrue(self.product.image.name.endswith('.webp'))

        # image field is a blankable and nullable field
        self.product.image = ''
        self.product.save()

        self.assertEqual(self.product.image, '')
    
    def test_product_banner_field_attributes_validation(self):
        # ensure that the banner file uploaded in its correct path
        self.assertTrue(self.product.banner.name.startswith('product_banners/'))

        # banner field is a blankable and nullable field
        self.product.banner = ''
        self.product.save()

        self.assertEqual(self.product.banner, '')
    
    def test_product_datetime_created_field_attributes_validation(self):
        # check if 'auto_now_add' behaviour works correctly
        product = Product.objects.create(
            name = 'product', 
            quantity = 1, 
            price = 10000,
            slug = 'product',
            category = self.category
        )

        self.assertEqual(product.datetime_created.replace(microsecond=0), timezone.now().replace(microsecond=0))

    def test_product_datetime_modified_field_attributes_validation(self):
        # check if 'auto_now' behaviour works correctly
        self.product.name = 'another name for this product'
        self.product.save()

        self.assertEqual(self.product.datetime_modified.replace(microsecond=0), timezone.now().replace(microsecond=0))
    
    def test_product_activation_field_attribute(self):
        # test default attribute
        self.assertTrue(self.product.activation)
    
    def test_product_feature_field_attribute(self):
        # test default attribute
        self.assertFalse(self.product.feature)


    # Model Relationship Testing
    
    def test_product_category_relation_to_product_model(self):
        # test Foreignkey relationship
        self.assertEqual(self.product.category, self.category)

        self.assertIn(self.product, self.category.products.all())

        # test on_delete method
        with self.assertRaises(ProtectedError):
            self.category.delete()
        
        # Verify that the reverse relation 'products' exists on the Category instance
        self.assertTrue(hasattr(self.category, 'products'))

        # Verify that the related name 'products' is correctly set on the Category instance
        related_manager = getattr(self.category, 'products')
        self.assertTrue(isinstance(related_manager, models.Manager))
    
    def test_product_user_wished_product_relation_to_product_model(self):
        # test ManytoManyField relationship
        self.assertIn(self.user, self.product.user_wished_product.all())

        self.assertIn(self.product, self.user.wished_product.all())

        # Verify that the reverse relation 'wished_product' exists on the User instance
        self.assertTrue(hasattr(self.user, 'wished_product'))

        # Verify that the related name 'wished_product' is correctly set on the User instance
        related_manager = getattr(self.user, 'wished_product')
        self.assertTrue(isinstance(related_manager, models.Manager))

        # user_wished_product is a blankable field
        self.product.user_wished_product.set([])
        self.product.save()

        self.assertQuerysetEqual(self.product.user_wished_product.all(), [])


    # Custom Method Testing
    
    def test_product_str_method(self):
        self.assertEqual(self.product.__str__(), self.product.name)
    
    def test_product_get_absolute_url_method(self):
        self.assertEqual(self.product.get_absolute_url(), reverse('products:product_detail', args=[self.product.slug]))
    
    def test_product_clean_price_method(self):
        self.assertEqual(self.product.clean_price(), f'{self.product.price: ,}')
    
    def test_product_out_of_stock_method(self):
        self.assertFalse(self.product.out_of_stock())

        self.product.quantity = 0
        self.product.save()

        self.assertTrue(self.product.out_of_stock())