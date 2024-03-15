from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderItem, Order
from products.models import Discount

@receiver(post_save, sender=OrderItem)
def decrease_product_quantity_of_order_items_product_that_submmited_as_order(sender, instance, created, **kwargs):
    if created:
        # because order_create view logic, first order is created then orderitem
        instance.product.quantity -= instance.quantity
        instance.product.save()
