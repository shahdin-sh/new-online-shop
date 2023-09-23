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
    # it determines the subcategory (children) of the category (parent)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    description = models.TextField(blank=True)


    # Custom Managers
    objects = models.Manager() # our default django manager
    is_featured_manager = IsFeatureManager()

    class Meta:
        # enforcing that there can not be two categories under a parent with same slug
        # __str__ method elaborated later in post.  use __unicode__ in place of
        # __str__ if you are using python 2

        unique_together = ('slug', 'parent',)
        verbose_name_plural = "categories"

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        # it means the main category have subcategory and that subcategory could have sub subcategory
        while k is not None:
            # k.name = self.parent.name
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])


class Product(models.Model):

    PRODUCT_QUALITY_CHOICES = (
        ('PERFECT', 'perfect'),
        ('GOOD', 'good'),
        ('NOT BAD', 'not bad'),
        ('BAD', 'bad'),
        ('VERY BAD', 'very bad')
    )

    name = models.CharField(max_length=200)
    description = RichTextField()
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    price = models.PositiveIntegerField()
    slug = models.SlugField(unique=True)
    size = models.CharField(max_length=200, null=True, blank=True)
    color = models.CharField(max_length=200, null=True, blank=True)
    quality = models.CharField(choices=PRODUCT_QUALITY_CHOICES, max_length=200)
    # problem with this default property
    image = models.ImageField(upload_to='product/', default='product_default/shopping_kart.jpg')
    datetime_created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='products')
    user_wished_product = models.ManyToManyField(get_user_model(), blank=True, related_name='wished_product')


    # Custom Managers
    objects = models.Manager() # our default django manager
    # is_featured_manager = IsFeatureManager()
    is_active_manager = IsActiveManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail_view', args=[self.pk])
    
    def clean_price(self):
        return f'{self.price: ,}'


class Comment(models.Model):
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    # author here is just users who signed in before! (authenticated users)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
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