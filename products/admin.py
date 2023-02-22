from django.contrib import admin
from .models import Category,Product, Comment
from .forms import SizeAndColorForm


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'category', 'is_active', 'is_featured', 'product_price']
    prepopulated_fields = {'slug': ('name',)}
    form = SizeAndColorForm

    def product_price(self, obj):
        return f"{obj.price:,} T"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_or_subcategory', 'parent', 'slug']
    ordering = ['is_featured']
    prepopulated_fields = {'slug': ('name',)}

    def category_or_subcategory(self, obj):
        # by returning the object, it displays __str__ method of our obj.
        return obj


class CommentAdmin(admin.ModelAdmin):
    list_display = ['content','author', 'product', 'parent', 'datetime_created', 'is_comment', 'rating']

    def is_comment(self, obj):
        if obj.parent:
            return f'replay of {obj.parent}'
        return 'comment'
 

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)