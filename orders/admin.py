from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from orders.models import Order, OrderItem, CustomerWithAddress
from django.db.models import Prefetch, F

# admin inlines
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['order', 'product', 'quantity', 'price', 'discounted_price']
    readonly_fields = fields
    classes = ('collapse', )
    can_delete = False

    @admin.display(description='discounted price ')
    def clean_discounted_price(self, obj):
        if obj.discounted_price != 0:
            return f"{obj.discounted_price: ,} T"
        return 0


class OrderInline(admin.TabularInline):
    model = Order
    fileds = ['datetime_created', 'datetime_modified', 'order_status']
    readonly_fields = fileds
    classes = ('collapse', )


# admin models
class OrderAdmin(admin.ModelAdmin):

    list_display = ['order_id','customer', 'showing_order_items', 'order_total_price', 'datetime_created', 'datetime_modified', 'order_status']
    list_filter = ['order_status']
    
    inlines = [
        OrderItemInline,
    ]

    @admin.action(description='order id')
    def order_id(self, obj):
        return f'order {obj.id}'

    def get_queryset(self, request):
        customer_prefetch = Prefetch('customer', queryset=CustomerWithAddress.objects.select_related('user'))
        return super().get_queryset(request).prefetch_related('items', customer_prefetch).all()

    @admin.action(description='order items')
    def showing_order_items(self, obj):
        url = reverse('admin:orders_orderitem_changelist') + '?' + urlencode({'order__id': obj.id})
        return format_html('<a href={}>{}</a>', url, obj.items.count())
    
    @admin.action(description='total price')
    def order_total_price(self, obj):
        return obj.intcomma(obj.get_order_total_price)
    


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'product_price','clean_discounted_price', 'clean_total_price', 'color', 'size', 'datetime_created']
    readonly_fields = list_display
    list_filter = ['order', 'order__customer']
    ordering = ['-order__datetime_created']

    def get_queryset(self, request):
        customer_prefetch = Prefetch('order__customer', queryset=CustomerWithAddress.objects.select_related('user'))
        return super().get_queryset(request).select_related('order', 'product').prefetch_related(customer_prefetch).annotate(total_price=F("price") * F("quantity"))

    def product_price(self, obj):
        return obj.intcomma(obj.price)
    
    @admin.display(description='discounted price ')
    def clean_discounted_price(self, obj):
        if obj.discounted_price != 0:
            return obj.intcomma(obj.discounted_price)
        return 0
    
    @admin.display(description='total price')
    def clean_total_price(self, obj):
        return obj.intcomma(obj.get_item_total_price)
    

class CustomerWithAddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'email', 'company', 'country', 'address', 'town' , 'zip_code', 'phone_number']
    list_filter = ['user']
    inlines = [
        OrderInline
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('orders').all()


# Register your models here.
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(CustomerWithAddress, CustomerWithAddressAdmin)