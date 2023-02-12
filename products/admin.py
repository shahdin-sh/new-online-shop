from django.contrib import admin
from .models import Category,Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'category', 'is_active', 'is_featured', 'price']
    prepopulated_fields = {'slug': ('name',)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_or_subcategory', 'parent', 'slug']
    ordering = ['is_featured']
    prepopulated_fields = {'slug': ('name',)}

    def category_or_subcategory(self, obj):
        # by returning the object, it displays __str__ method of our obj.
        return obj


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)

