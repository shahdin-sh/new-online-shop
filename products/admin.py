from django.contrib import admin
from .models import Category,Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'category', 'is_active', 'price']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'subcategory_name', 'parent']


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)

