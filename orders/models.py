from django.db import models
from accounts.models import CustomUserModel


class Order(models.Model):
    customer = models.OneToOneField(CustomUserModel, on_delete=models.SET_NULL, related_name='order', null=True)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    company = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    town = models.CharField(max_length=20)
    area = models.CharField(max_length=20)
    zip_code = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=200)
    note = models.TextField(blank=True)
    is_paid = models.BooleanField(default=False)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.customer} order| id:{self.id}'
    
    def get_total_price(self):
        return sum(item.price * item.quantity for item in self.items.all()) 
    
    def get_order_items(self):
        return self.items.all()
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.order} items'
    
    def product_price(self, obj):
        return f"{obj.price:,} T"
    
    def total_price(self):
        return f"{self.price * self.quantity:,}"