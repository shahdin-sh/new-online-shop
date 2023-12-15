from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['order', 'product', 'quantity', 'price']
    readonly_fields = fields
    classes = ('collapse', )
    can_delete = False
    show_change_link = True


class OrderAdmin(admin.ModelAdmin):

    list_display = ['customer', 'first_name', 'last_name', 'datetime_created', 'order_status']
    list_filter = ['order_status']
    
    inlines = [
        OrderItemInline,
    ]



class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'product_price', 'total_price', 'color', 'size', 'datetime_created']
    readonly_fields = list_display

    def product_price(self, obj):
        return f"{obj.price:,} T"
    
    def total_price(self, obj):
        return f"{obj.product.price * obj.quantity:,} T"


# Register your models here.
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)