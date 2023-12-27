from django.db import models
from accounts.models import CustomUserModel


class CustomerWithAddress(models.Model):

    COUNTRY_CHOICES = (
        ('TURKEY', 'turkey'),
        ('IRAN', 'iran'),
        ('IRAQ', 'iraq'),
        ('BAHRAIN','bahrain'),
        ('UAE', 'united arabic emirates')
    )

    user = models.OneToOneField(CustomUserModel, on_delete=models.PROTECT, related_name='customer_info')
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

        ('p', 'PAID'),
        ('u', 'UNPAID'),
        ('c', 'CANCELED')
    )

    customer = models.ForeignKey(CustomerWithAddress, on_delete=models.PROTECT, related_name='orders', blank=True, null=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    order_status = models.CharField(max_length=100, choices=ORDERS_STATUS_CHOICES, default='u')


    def __str__(self):
        return f'order_id {self.id} for {self.customer}'

    def get_total_price(self):
        return sum(item.price * item.quantity for item in self.items.all())
    
    def get_order_items(self):
        return self.items.all()
    
    

class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()
    color = models.CharField(max_length=200, default='black')
    size = models.CharField(max_length=200, default='large')
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.order} items'
    
    def product_price(self, obj):
        return f"{obj.price:,} T"
    
    def total_price(self):
        return f"{self.price * self.quantity:,}"

