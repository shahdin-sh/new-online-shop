import string
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import DataError as django_db_dataerror
from django.db.utils import DatabaseError
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

    def test_discount_promo_code_and_type_fields_attributes(self):
        # promo code is a blankable field
        self.percentage_discount.promo_code = ''
        self.percentage_discount.save()

    
        self.fixed_amount_discount.promo_code = ''
        self.fixed_amount_discount.save()

        # test type choices
        for choice in Discount.DISCOUNT_TYPE_CHOICES:
            self.percentage_discount.type = choice
            self.percentage_discount.save()

            self.assertEqual(self.percentage_discount.type, choice)

            self.fixed_amount_discount.type = choice
            self.fixed_amount_discount.save()

            self.assertEqual(self.fixed_amount_discount.type, choice)
    
    def test_discount_value_and_percent_fields_attributes(self):
        # vlaue field is nullable and blankable field
        self.fixed_amount_discount.value = None
        self.fixed_amount_discount.save()

        self.assertEqual(self.fixed_amount_discount.value, None)
        self.assertIsNone(self.percentage_discount.value)

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

    def test_description_and_expiration_date_and_status_fields_attributes(self):
        # test choices attribute from status field
        for choice in Discount.DISCOUNT_STATUS_CHOICES:
            self.percentage_discount.status = choice
            self.percentage_discount.save()

            self.assertEqual(self.percentage_discount.status, choice)

            self.fixed_amount_discount.status = choice
            self.fixed_amount_discount.save()

            self.assertEqual(self.fixed_amount_discount.status, choice)
        
        # test default attribute for expiration_date field
        discount_obj = Discount.objects.create(
            type = Discount.FIXED_AMOUNT_DISCOUNT,
            value = 100000,
            percent = None,
            description = '',
            status = Discount.ACTIVE
        )

        ten_days_from_now = (timezone.now() + timezone.timedelta(days=10)).replace(minute=0, second=0, microsecond=0) 
        self.assertEqual(discount_obj.expiration_date.replace(minute=0, second=0, microsecond=0), ten_days_from_now)


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
            
    def test_generate_promo_code_automation_when_object_created(self):
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
    
    def test_promo_code_manually_creation_status(self):

        with self.assertRaises(Discount.DoesNotExist):
            Discount.objects.create(
                promo_code = 'ABCD',
                type = Discount.FIXED_AMOUNT_DISCOUNT,
                value = 100000,
                description = 'random description for discount',
                status = Discount.ACTIVE
            )


    # Test Custom Validations
            
    def test_expiration_date_clean_method_condition(self):
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
    
    def test_type_field_relation_to_value_and_percent_field_clean_method_condition(self):
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