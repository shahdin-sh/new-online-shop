from django.contrib import admin
from .models import Category,Product, Comment, Discount
import random, string

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
    readonly_fields =  ['name', 'quantity', 'product_price', 'is_active', 'is_featured']
    extra = 1
    classes = ('collapse', )
    can_delete = False
    show_change_link = True

    def product_price(self, obj):
        return f"{obj.price:,} T"


class RepliesInline(admin.TabularInline):
    model = Comment
    verbose_name = 'Replies'
    readonly_fields =  ['content','author', 'email', 'name', 'rating']
    extra = 1
    classes = ('collapse', )
    can_delete = False
    show_change_link = True

# End Inlines


# start registering models
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    ordering = ['is_featured']
    prepopulated_fields = {'slug': ('name',)}

    def category_or_subcategory(self, obj):
        # by returning the object, it displays __str__ method of our obj.
        return obj


class DiscountAdmin(admin.ModelAdmin):
    list_display = ['promo_code', 'discount_type', 'clean_value', 'description', 'expiration_date']

    def clean_value(self, obj):
        return obj.clean_value()   

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'category', 'is_active', 'is_featured', 'product_price', 'datetime_created', 'size', 'color']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['-datetime_created']
    inlines = [
        CommentsInline,
    ]

    def product_price(self, obj):
        return f"{obj.price:,} T"


class CommentAdmin(admin.ModelAdmin):
    list_display = ['content','author', 'name', 'email', 'product', 'datetime_created', 'is_comment', 'is_spam', 'rating', 'session_token']
    ordering = ['-datetime_created']
    inlines = [
        RepliesInline
    ]

    def get_queryset(self, request):
        # Get the original queryset from the parent class
        queryset = super().get_queryset(request)

        # Filter the comments to show only comments  (comments without parents)
        queryset = queryset.filter(parent__isnull=True)

        return queryset

    def is_comment(self, obj):
        if obj.parent:
            return f'replay of {obj.parent}'
        return 'comment'
# end registering models 

# registering admin sites
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Discount, DiscountAdmin)