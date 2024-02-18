from typing import Any
from django.contrib import admin
from django.db.models import Count, Subquery, OuterRef, CharField
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from django.utils.http import urlencode
from products.models import Category,Product, Comment, Discount


# filters

class InventoryFilter(admin.SimpleListFilter):
    # const values
    LESS_THAN_3 = '<3'
    BETWEEN_3_AND_10 = '3<>10'
    LEES_THAN_10 = '<10'

    title = 'Critical Inventory Status'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            (InventoryFilter.LESS_THAN_3, 'High'),
            (InventoryFilter.BETWEEN_3_AND_10, 'Medium'),
            (InventoryFilter.LEES_THAN_10 , 'ok')
        ]

    def queryset(self, request, queryset):
        if self.value() == InventoryFilter.LESS_THAN_3:
            return queryset.filter(quantity__lt=3)
        if self.value() == InventoryFilter.BETWEEN_3_AND_10:
            return queryset.filter(quantity__range=(3, 10))
        if self.value() == InventoryFilter.LESS_THAN_3:
            return queryset.filter(quantity__lt=10)


class ProductAmountFilter(admin.SimpleListFilter):
    # const values
    LESS_THAN_10_PRODUCT = '<10'
    BETWEEN_10_TO_20_PRODUCT = '10<=20'
    More_THAN_20_PEODUCT = '>20'

    title = ('Product Amount')
    parameter_name = 'product_amount_filter'

    def lookups(self, request, model_admin):
        return [
            (ProductAmountFilter.LESS_THAN_10_PRODUCT, 'Less than 10 product'),
            (ProductAmountFilter.BETWEEN_10_TO_20_PRODUCT, 'In range of 10, 20 product'),
            (ProductAmountFilter.More_THAN_20_PEODUCT, 'More than 20 product'),
        ]

    def queryset(self, request, queryset):
        if self.value() == ProductAmountFilter.LESS_THAN_10_PRODUCT:
            return queryset.filter(products_count__lt=10)
        if self.value() == ProductAmountFilter.BETWEEN_10_TO_20_PRODUCT:
            return queryset.filter(products_count__range=(10, 20))
        if self.value() == ProductAmountFilter.More_THAN_20_PEODUCT:
            return queryset.filter(products_count__gt=20)


class ProductImageFilter(admin.SimpleListFilter):
    # const values
    PRODUCT_WITH_IMAGE = 'if_image'
    PRODUCT_WITHOUT_IMAGE = 'if_not_image'

    title = ('Product Image Status')
    parameter_name = 'product_image_filter'

    def lookups(self, request, model_admin):
        return [
            (ProductImageFilter.PRODUCT_WITH_IMAGE, 'With Image'),
            (ProductImageFilter.PRODUCT_WITHOUT_IMAGE, 'With Out Image'),
        ] 

    def queryset(self, request, queryset):
        if self.value() == ProductImageFilter.PRODUCT_WITH_IMAGE:
            return queryset.filter(image__isnull=False)
        if self.value() == ProductImageFilter.PRODUCT_WITHOUT_IMAGE:
            return queryset.filter(image__isnull=True)



# Start Inlines
class CommentsInline(admin.TabularInline):
    model = Comment
    readonly_fields = ['content','author', 'email', 'name', 'parent', 'rating']
    extra = 1
    classes = ('collapse',)
    can_delete = False
    show_change_link = True

    def is_comment(self, obj):
        if obj.parent:
            return f'replay of {obj.parent}'
        return 'comment'
 


class ProductsInline(admin.TabularInline):
    model = Product
    fields =  ['name', 'quantity', 'price', 'activation', 'feature']
    extra = 0
    classes = ('collapse', )
    can_delete = False
    show_change_link = True


class RepliesInline(admin.TabularInline):
    model = Comment
    verbose_name = 'Replies'
    readonly_fields =  ['content','author', 'email', 'name', 'rating']
    extra = 1
    classes = ('collapse', )
    can_delete = False
    show_change_link = True

# End Inlines


# Start Registering Models

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_featured', 'description', 'product_amount', 'selected_product']
    ordering = ['is_featured']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 10
    search_fields = ['name']
    inlines = [
        ProductsInline,
    ]
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('products').annotate(products_count=Count('products'))

    def product_amount(self, obj):
        return obj.products.all().count()

    def get_list_filter(self, request):
        return [ProductAmountFilter] 


class DiscountAdmin(admin.ModelAdmin):
    list_display = ['promo_code', 'type','discount_product', 'clean_value', 'clean_percent', 'description', 'expiration_date', 'status', 'datetime_created', 'datetime_modified']
    list_display_links = ['promo_code', 'type']
    readonly_fields = ['promo_code']
    list_filter = ['expiration_date', 'status']
    list_per_page = 10
    search_fields = ['promo_code']
    actions = ['convert_to_deactive_status']
    
    def save_model(self, request, obj, form, change): 
        if obj.expiration_date < timezone.now():
            obj.status = Discount.DEACTIVE
        return super().save_model(request, obj, form, change)


    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('products').annotate(
            discount_products=
            Subquery(Product.objects.filter(discounts=OuterRef('pk')).values_list('name', flat=True)[:1], 
                     output_field=CharField()
            ))

    def clean_value(self, obj):
        if obj is not None:
            return obj.clean_value()
        return None
    
    def clean_percent(self, obj):
        if obj.percent:
            return f'{obj.percent} %'
        return obj.percent
    
    @admin.display(description='products')
    def discount_product(self, obj):
        url = reverse('admin:products_product_changelist') + '?' + urlencode({'discounts__id': obj.id})
        return format_html('<a href={}>{}</a>', url, obj.products.count())
    
    @admin.action(description='Convert to deactive status')
    def convert_to_deactive_status(self, request, queryset):
        update_count  = queryset.update(status=Discount.DEACTIVE)
        self.message_user(request, f"Successfully convert {update_count} discount's status to deactive.")


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'product_category', 'comments_amount', 'activation', 'feature', 'product_price', 'datetime_created', 'datetime_modified', 'size', 'color']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['-datetime_created']
    list_select_related = ['category']
    search_fields = ['name']
    list_per_page = 20
    list_filter = ['datetime_created', InventoryFilter, ProductImageFilter]
    actions = [
        'clean_inventory',
    ]
    autocomplete_fields = ['category', ]

    inlines = [
        CommentsInline,
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('comments')

    def product_price(self, obj):
        return f"{obj.price:,} T"
    
    def product_category(self, obj):
        return obj.category.name
    
    @admin.display(description='comments')
    def comments_amount(self, obj):
        url = (reverse('admin:products_comment_changelist')  + '?' + urlencode({'product__id': obj.id}))
        return format_html("<a href='{}'>{}</a>", url,  obj.comments.count())
    
    @admin.action(description='Clean products inventory.')
    def clean_inventory(self, request, queryset):
        update_count = queryset.update(quantity=0)
        if update_count == 1:
            self.message_user(request, f"Successfully cleared {update_count} product's invetory to zeros.")
        else:
            self.message_user(request, f"Successfully cleared {update_count} product's invetories to zeros.")


class CommentAdmin(admin.ModelAdmin):
    list_display = ['get_content_summary', 'author', 'name', 'email', 'product', 'datetime_created', 'is_spam', 'rating', 'session_token']
    list_per_page = 10
    list_filter = ['is_spam']
    search_fields = ['author', 'name', 'email']
    ordering = ['author']

    inlines = [
        RepliesInline
    ]
    autocomplete_fields = ['product', ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('author').filter(parent__isnull=True)

# End registering models 


# registering admin sites
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Discount, DiscountAdmin)