from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class CustomerWithAddress(models.Model):

    COUNTRY_CHOICES = (
        ('TURKEY', 'turkey'),
        ('IRAN', 'iran'),
        ('IRAQ', 'iraq'),
        ('BAHRAIN','bahrain'),
        ('UAE', 'united arabic emirates')
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='customer_info')
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    company = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=250, choices=COUNTRY_CHOICES)
    address = models.CharField(max_length=200)
    town = models.CharField(max_length=20)
    zip_code = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=200)
    note = models.TextField(blank=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'customer:{self.user}'


class Order(models.Model):

    ORDERS_STATUS_CHOICES = (

        ('Paid', 'PAID'),
        ('Unpaid', 'UNPAID'),
        ('Canceled', 'CANCELED')
    )

    customer = models.ForeignKey(CustomerWithAddress, on_delete=models.PROTECT, related_name='orders', blank=True, null=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=100, choices=ORDERS_STATUS_CHOICES, default='Unpaid')
    paid_signal = models.BooleanField(default=False)
    canceled_signal = models.BooleanField(default=False)


    def __str__(self):
        return f'order_id {self.id} for {self.customer}'
    
    def intcomma(self, value):
        return f'{value:,} T'

    @property
    def get_order_total_price(self): 
        return sum([item.get_item_total_price for item in self.items.all()])
    
    @property
    def get_order_items(self):
        return self.items.all()
    

class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, related_name='order_items', null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()
    discounted_price = models.PositiveBigIntegerField(default=0)
    color = models.CharField(max_length=200, default='black')
    size = models.CharField(max_length=200, default='large')
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['order', 'product']]

    def __str__(self):
        return f'{self.order} items'
    
    def intcomma(self, value):
        return f'{value:,} T'
    
    @property
    def get_item_total_price(self):
        if self.discounted_price != 0:
            discounted_total_price = self.quantity * self.discounted_price
            return discounted_total_price
        
        total_price = self.quantity * self.price
        return total_price