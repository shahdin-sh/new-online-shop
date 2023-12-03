from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .models import Category,Product, Comment, Discount
import random, string
from django.db.models import Count

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
    fields =  ['name', 'quantity', 'price', 'is_active', 'is_featured']
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


# start registering models

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_featured', 'description']
    ordering = ['is_featured']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [
        ProductsInline,
    ]


class DiscountAdmin(admin.ModelAdmin):
    list_display = ['promo_code', 'type', 'clean_value', 'clean_percent', 'description', 'expiration_date', 'status']

    def clean_value(self, obj):
        if obj is not None:
            return obj.clean_value()
        return None
    
    def clean_percent(self, obj):
        if obj.percent:
            return f'{obj.percent} %'
        return obj.percent

    # def clean_percent(self,obj):
    #     return obj.clean_percent()   

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'category', 'activation', 'feature', 'product_price', 'datetime_created', 'size', 'color']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['-datetime_created']
    inlines = [
        CommentsInline,
    ]

    def product_price(self, obj):
        return f"{obj.price:,} T"


class CommentAdmin(admin.ModelAdmin):
    list_display = ['get_content_summary', 'author', 'name', 'email', 'product', 'datetime_created', 'is_comment', 'is_spam', 'rating', 'session_token']
    ordering = ['author']
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