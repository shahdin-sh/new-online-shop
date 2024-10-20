import factory
import random
import string
from django.contrib.auth import get_user_model 
from django.utils import timezone
from datetime import datetime
from factory.django import DjangoModelFactory
from faker import Faker
from products import models

fake = Faker()


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = models.Category

    name = factory.LazyFunction(lambda: ' '.join(x for x in fake.words(2)))
    slug = factory.LazyAttribute(lambda obj: '-'.join(obj.name.split(' ')).lower())
    is_featured = factory.Faker("boolean")
    description = factory.Faker('paragraph', nb_sentences=1, variable_nb_sentences=False)


class DiscountFactory(DjangoModelFactory):
    class Meta:
        model = models.Discount

    # promo_code = factory.LazyFunction(lambda: ''.join(random.choice(string.ascii_letters.upper()) for _ in range(4)))
    type = factory.LazyFunction(lambda: random.choice([choice[0] for choice in models.Discount.DISCOUNT_TYPE_CHOICES]))
    value = None
    percent = None
    description = factory.Faker('paragraph', nb_sentences=1, variable_nb_sentences=False)
    expiration_date = factory.LazyFunction(lambda: fake.date_time_ad(start_datetime=timezone.datetime(2023, 11, 29), end_datetime=timezone.datetime(2024, 1, 1), tzinfo=timezone.get_current_timezone()))

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        discount_type = kwargs.get('type', None)
        if discount_type == models.Discount.FIXED_AMOUNT_DISCOUNT:
            # if discount type be fixed amount discount

            kwargs['value'] = random.randint(100000, 1000000)
            kwargs['percent'] = None

        elif discount_type == models.Discount.PERCENTAGE_DISCOUNT:
            # if discount type be percentage discount
            kwargs['percent'] = round(random.uniform(10, 99), 1)
            kwargs['value'] = None
            
        return super(DiscountFactory, cls)._create(model_class, *args, **kwargs)


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = models.Product

    name = factory.LazyFunction(lambda: ' '.join(x for x in fake.words(2)))
    description = factory.Faker('paragraph', nb_sentences=5, variable_nb_sentences=False)
    quantity = factory.LazyFunction(lambda: random.randint(1, 100)) # or factory.Faker('random-int', min=0, max=100) or factory.Faker('random-element', elements=[i for i in range(1, 101)])
    feature = factory.Faker("boolean")
    price = factory.LazyFunction(lambda: random.randint(100000, 5000000))
    slug = factory.LazyAttribute(lambda obj: '-'.join(obj.name.split(' ')).lower())
    size = factory.LazyFunction(lambda: random.choice([size[0] for size in models.Product.SIZE_CHOICES]))
    color = factory.LazyFunction(lambda: random.choice([color[0] for color in models.Product.COLOR_CHOICES]))
    datetime_created = factory.LazyFunction(datetime.now)
    discounts = factory.SubFactory(DiscountFactory)


    @factory.post_generation
    def user_wished_product(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for user in extracted:
                self.user_wished_product.add(user)
    
    @factory.post_generation
    def discounts(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted: 
            for discount in extracted:
                self.discounts.add(discount)


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = models.Comment


    content = factory.Faker('paragraph', nb_sentences=3, variable_nb_sentences=True)
    datetime_created = factory.LazyFunction(datetime.now)
    rating = factory.LazyFunction(lambda: random.choice([choice[0] for choice in models.Comment.RATING_CHOICES]))
    author = None
    name = None
    email = None

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # Custom logic to handle author field based on the random choice
        if random.choice([True, False]):
            kwargs['author'] = random.choice(list(get_user_model().objects.all()))
        else:
            kwargs['name'] = fake.first_name()
            kwargs['email'] = fake.email()

        return super(CommentFactory, cls)._create(model_class, *args, **kwargs)
    # datetime_modified, parent, session_token