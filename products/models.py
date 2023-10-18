from django.db import models
from django.shortcuts import reverse
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from accounts.models import CustomUserModel


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


    # Custom Managers
    objects = models.Manager() # our default django manager
    is_featured_manager = IsFeatureManager()
    is_active_manager = IsActiveManager()

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
    rating = models.PositiveIntegerField(null=True, blank=True)


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