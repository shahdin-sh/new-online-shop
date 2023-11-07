import string, random
from django.db import models
from django.shortcuts import reverse
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from accounts.models import CustomUserModel
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


# managers
class IsFeatureManager(models.Manager):
    
    def get_queryset(self):
        return super(IsFeatureManager, self).get_queryset().filter(is_featured=False)           

class IsActiveManager(models.Manager):
    def get_queryset(self):
        return super(IsActiveManager, self).get_queryset().filter(is_active=True)


class IsOrderManager(models.Manager):
    def get_queryset(self):
        return super(IsOrderManager, self).get_queryset().order_by('-datetime_created')
    

class IsNotSpamManager(models.Manager):
    
    def get_queryset(self):
        return super(IsNotSpamManager, self).get_queryset().filter(is_spam=False)
    

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    is_featured = models.BooleanField(null=True, default=False)
    description = models.TextField(blank=True)


    # Custom Managers
    objects = models.Manager() # our default django manager
    is_featured_manager = IsFeatureManager()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('products:category_detail', args=[self.slug])
    

class Discount(models.Model):

    DISCOUNT_TYPE_CHOICES = (
        ('PD', 'PERCENTAGE DISCOUNT'),
        ('FAD', 'FIXED AMOUNT DISCOUNT'),
        ('BOGO', 'BUY ONE GET ONE'),
    )

    DISCOUNT_STATUS_CHOICES = (
        ('AC', 'ACTIVE'),
        ('DC', 'DEACTIVE'),
    )
    promo_code = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=255, choices=DISCOUNT_TYPE_CHOICES)
    value = models.PositiveIntegerField(blank=True, null=True)
    percent = models.DecimalField(max_digits=3, decimal_places=1, validators=[MaxValueValidator(limit_value=100), MinValueValidator(limit_value=1)], blank=True, null=True)
    description = models.CharField(max_length=100)
    expiration_date = models.DateTimeField()
    status = models.CharField(max_length=255, choices=DISCOUNT_STATUS_CHOICES, default='AC')

    def __str__(self):
        return f'{self.promo_code} discount'

    def clean_value(self):
        if self.value is not None:
            return f'{self.value: ,} T'    
    
    def clean_percent(self):
        if self.percent is not None:
            return f'{self.value: ,} %'    

    def check_and_delete_if_expired(self):
        if self.expiration_date < timezone.now():
            self.delete()

    def save(self, *args, **kwargs):
        # generate promo code if the discount is percenatage discount or fixed amount discount.
        if not self.promo_code:
            if self.type != 'BOGO':
                letters = string.ascii_letters.upper()
                digits = ''.join(random.choice(letters) for _ in range(4))
                self.promo_code  = digits
        super(Discount, self).save(*args, **kwargs)
    

class Product(models.Model):

    PRODUCT_QUALITY_CHOICES = (
        ('PERFECT', 'perfect'),
        ('GOOD', 'good'),
        ('NOT BAD', 'not bad'),
        ('BAD', 'bad'),
        ('VERY BAD', 'very bad')
    )

    COLOR_CHOICES = (
        ('BLACK', 'black'),
        ('WHITE', 'white'),
        ('PINK', 'pink'),
    )

    SIZE_CHOICES = (
        ('LARGE', 'large'),
        ('MEDIUM', 'medium'),
        ('SMALL', 'small'),
    )

    name = models.CharField(max_length=200)
    description = RichTextField()
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    # price = 120,000 t or 1,000,000 t or 3,456,990 t
    price = models.PositiveIntegerField()
    slug = models.SlugField(unique=True)
    size = models.CharField(choices=COLOR_CHOICES, max_length=200, null=True, blank=True)
    color = models.CharField(choices=SIZE_CHOICES, max_length=200, null=True, blank=True)
    quality = models.CharField(choices=PRODUCT_QUALITY_CHOICES, max_length=200)
    image = models.ImageField(upload_to='product/', default='product_default/shopping_kart.jpg')
    banner = models.ImageField(upload_to='product/', default='product/bn3-1.webp')
    datetime_created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='products')
    user_wished_product = models.ManyToManyField(get_user_model(), blank=True, related_name='wished_product')
    discounts = models.ManyToManyField(Discount, related_name='products')


    # Custom Managers
    objects = models.Manager() # our default django manager
    is_featured_manager = IsFeatureManager()
    is_not_spam_manager = IsNotSpamManager()

    def save(self, *args, **kwargs):
        # Check if the quantity is 0, and if so, set is_active to False
        if self.quantity == 0:
            self.is_active = False
        else:
            self.is_active = True
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.slug])
    
    def clean_price(self):
        return f'{self.price: ,}'



class Comment(models.Model):

    RATING_CHOICES = (
        ('POOR', 'poor'),
        ('BAD', 'bad'),
        ('NORMAL', 'normal'),
        ('GOOD', 'good'),
        ('PERFECT', 'perfect'),
    )

    content = models.TextField()
    is_spam = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    # author here is just users who signed in before! (authenticated users)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='product_comments', blank=True, null=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    parent = models.ForeignKey('self' , null=True , blank=True , on_delete=models.CASCADE , related_name='replies')
    session_token = models.CharField(max_length=32, null=True, blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    rating = models.CharField( max_length=100, choices=RATING_CHOICES, null=True, blank=True)


    # Custom Managers
    objects = models.Manager() # our default django manager
    is_active_manager = IsActiveManager()
    is_order_manager = IsOrderManager

    def __str__(self):
        return self.content

    @property
    def children(self):
        return Comment.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False