from django.db import transaction
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

from .models import OrderItem, Order
from products.models import Product


@receiver(post_save, sender=Order)
def decresed_product_amount_after_successful_payment(sender, instance, created, **kwargs):

    order_instance = Order.objects.filter(pk=instance.pk)

    if created:
        order_instance.update(paid_signal=True)
        
    products_to_update = []

    for item in instance.items.all():
        if instance.status == 'Paid' and instance.paid_signal:
            item.product.quantity -= item.quantity
            order_instance.update(canceled_signal=True)
            order_instance.update(paid_signal=False)

        elif instance.status == 'Canceled' and instance.canceled_signal:
            item.product.quantity += item.quantity
            order_instance.update(paid_signal=True)
            order_instance.update(canceled_signal=False)

        products_to_update.append(item.product)
     
    with transaction.atomic():
        Product.objects.bulk_update(products_to_update, ['quantity'])


@receiver(pre_delete, sender=Order)
def restore_product_amount_after_order_deletion(sender, instance, **kwargs):
    if instance.status == 'Paid':
        products_to_update = []

        for item in instance.items.all():
            item.product.quantity += item.quantity
            products_to_update.append(item.product)

        Product.objects.bulk_update(products_to_update, ['quantity'])
    



# user add a product to cart after creation order item 
# if order is paid the quantity should be reduced 
# if order items get delete all the quantity should be restored
# handle product quantity in template