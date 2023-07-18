from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['order', 'product', 'quantity', 'price']
    readonly_fields = ['order', 'product', 'quantity', 'price'] 
    extra = 1
    classes = ('collapse', )
    can_delete = False
    show_change_link = True



class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'name', 'last_name', 'is_paid', 'datetime_created']
    # ordering = ['datatime_created']
    inlines = [
        OrderItemInline,
    ]



class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'datetime_created']
    # ordering = ['datetime_created']



# Register your models here.
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)