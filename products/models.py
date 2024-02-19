import string, random
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from ckeditor.fields import RichTextField


# managers
# class ProductManager(models.Manager):

#     def activation(self):
#         return self.get_queryset().filter(activation=True)


class AcitveProduct(models.Manager):
    def get_queryset(self):
        return super(AcitveProduct, self).get_queryset().filter(activation=True)
    

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
    # # sample of circular dependecy
    selected_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')


    # Custom Managers
    objects = models.Manager() # our default django manager

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('products:category_detail', args=[self.slug])
    

class Discount(models.Model):
    # constant values for discount type choices
    PERCENTAGE_DISCOUNT = 'PD'
    FIXED_AMOUNT_DISCOUNT = 'FAD'

    # constant values for discount status choices
    ACTIVE = 'AC'
    DEACTIVE = 'DC'

    DISCOUNT_TYPE_CHOICES = (
        (PERCENTAGE_DISCOUNT, 'PERCENTAGE DISCOUNT'),
        (FIXED_AMOUNT_DISCOUNT, 'FIXED AMOUNT DISCOUNT'),
    )

    DISCOUNT_STATUS_CHOICES = (
        (ACTIVE, 'ACTIVE'),
        (DEACTIVE, 'DEACTIVE'),
    )

    promo_code = models.CharField(max_length=4, blank=True)
    type = models.CharField(max_length=255, choices=DISCOUNT_TYPE_CHOICES)
    value = models.PositiveIntegerField(blank=True, null=True)
    percent = models.DecimalField(max_digits=3, decimal_places=1, validators=[MaxValueValidator(limit_value=100), MinValueValidator(limit_value=1)], blank=True, null=True)
    description = models.CharField(max_length=100)
    expiration_date = models.DateTimeField(default=(timezone.now() + timezone.timedelta(days=10)).replace(hour=0, minute=0, second=0, microsecond=0))
    status = models.CharField(max_length=255, choices=DISCOUNT_STATUS_CHOICES, default='AC')
    datetime_created = models.DateField(auto_now_add=True, blank=True, null=True)
    datetime_modified = models.DateField(auto_now=True, blank=True, null=True)
    

    def __str__(self):
        return f'{self.promo_code} | {self.description}'

    def clean_value(self):
        if self.value is not None:
            return f'{self.value: ,} T'    
    
    def clean_percent(self):
        if self.percent is not None:
            return f'{self.percent: ,} %'    

    def check_and_delete_if_expired(self):
        if self.expiration_date <= timezone.now():
            self.delete()

    def save(self, *args, **kwargs):
        # generate promo code when object is being created
        if not self.promo_code and self.pk == None:
            letters = string.ascii_letters.upper()
            promo_code = ''.join(random.choice(letters) for _ in range(4))
            self.promo_code  = promo_code
        else:
             previous_promo_code = Discount.objects.get(pk=self.pk).promo_code
             self.promo_code = previous_promo_code

        super(Discount, self).save(*args, **kwargs)
    
    def clean(self):
        super().clean
        if self.expiration_date <= timezone.now():
            raise ValidationError('Expiration date can not be earlier than the current time.')
        
        # if value field is filled, set percent field to None and via versa
        if self.value and self.percent is not None:
            raise ValidationError('Only one percent or value can be filled.', code='invalid', params={})
        
        if self.type == Discount.PERCENTAGE_DISCOUNT and self.value is not None:
            raise ValidationError(f'Value field is not allowed to fill when type is {Discount.PERCENTAGE_DISCOUNT}')
        elif self.type == Discount.FIXED_AMOUNT_DISCOUNT and self.percent is not None:
            raise ValidationError(f'Percent field is not allowed to fill when type is {Discount.FIXED_AMOUNT_DISCOUNT}')


class Product(models.Model):

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
    description = RichTextField(blank=True, null=True)
    quantity = models.IntegerField(validators=[MaxValueValidator(limit_value=100), MinValueValidator(limit_value=0)])
    # price = 120,000 t or 1,000,000 t or 3,456,990 t
    price = models.PositiveIntegerField(validators=[MaxValueValidator(limit_value=10000000), MinValueValidator(limit_value=1000)])
    slug = models.SlugField(unique=True)
    size = models.CharField(choices=COLOR_CHOICES, max_length=200, default=SIZE_CHOICES[0])
    color = models.CharField(choices=SIZE_CHOICES, max_length=200, default=COLOR_CHOICES[0])
    image = models.ImageField(upload_to='product/', null=True, blank=True)
    banner = models.ImageField(upload_to='product_banners/', null=True, blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    user_wished_product = models.ManyToManyField(get_user_model(), blank=True, related_name='wished_product')
    discounts = models.ManyToManyField(Discount, related_name='products', blank=True)
    activation = models.BooleanField(default=True)
    feature = models.BooleanField(default=False)


    # Custom Managers
    # objects = PorductManager()
    objects = models.Manager()
    is_active = AcitveProduct()

    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.slug])
    
    def clean_price(self):
        return f'{self.price: ,}'
    
    def out_of_stock(self):
        if self.quantity == 0:
            return True
        return False




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
    name = models.CharField(max_length=250, null=True, blank=True)
    email = models.CharField(max_length=250, blank=True, null=True)
    parent = models.ForeignKey('self' , null=True , blank=True , on_delete=models.CASCADE , related_name='replies')
    session_token = models.CharField(max_length=32, null=True, blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    rating = models.CharField( max_length=100, choices=RATING_CHOICES, null=True, blank=True)


    # Custom Managers
    objects = models.Manager() # our default django manager
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
    
    def get_content_summary(self):
        result = ''
        for char in self.content:
            if char == '.':
                break
            result += char
        return result