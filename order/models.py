from django.db import models
from accounts.models import CustomUserModel


class Order(models.Model):
    customer = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    company = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    town = models.CharField(max_length=20)
    zip_code = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=200)
    note = models.TextField(blank=True)
    is_paid = models.BooleanField(default=False)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.customer} order| id:{self.id}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.order} items'
    