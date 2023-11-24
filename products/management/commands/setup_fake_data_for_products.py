from faker import Faker
import string
import random
from typing import Any
from django.core.management import BaseCommand
from products.factories import CategoryFactory, ProductFactory, DiscountFactory, CommentFactory
from products.models import Category, Product, Discount, Comment
from datetime import timedelta
from django.db import transaction
from cart.cart import Cart

fake = Faker()

list_of_models = [Category, Product, Discount, Comment]
# define the number of object that should generate for our models
NUM_CATEGORIES = 10
NUM_PRODUCTS_BASED_ON_CATEGORY = 100
NUM_DISCOUNTS = 20


class Command(BaseCommand):

    help = 'Populate database with fake data.'

    @transaction.atomic
    def handle(self, *args: Any, **options: Any):
        # deleting the old data and the cart data
        self.stdout.write('Deleting existing instances...')
        for model in list_of_models:
            model.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Deletion Complete...'))

        # categories data
        print(f'Adding {NUM_CATEGORIES} Categories...', end='')
        categories = [CategoryFactory() for _ in range(NUM_CATEGORIES)]
        print('Done')

        # discounts data
        print(f'Adding {NUM_DISCOUNTS} Discounts...', end='')
        discounts = [DiscountFactory() for _ in range(NUM_DISCOUNTS)]
        print('Done')

        # products data
        print(f'Adding {NUM_PRODUCTS_BASED_ON_CATEGORY} Products...', end='')
        all_products = list()
        for _ in range(NUM_PRODUCTS_BASED_ON_CATEGORY):
            product = ProductFactory(category=random.choice(categories), image='product\single-product-01.webp', banner='prodcut_banners\m4.webp')
            all_products.append(product)
        print('Done')


        # comment data
        print(f'Adding 10 comment for each product...', end='')
        for product in all_products:
            for _ in range(random.randint(1, 10)):
                comment = CommentFactory(product=product, is_spam=False)
                # creating session_token when the none authenticated user wants to add a comment.
                if comment.author is None:
                    comment.session_token = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
                comment.datetime_modified = comment.datetime_created + timedelta(hours=random.randint(1, 5000))
                comment = None
        print('Done')
            
