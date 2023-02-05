from django.contrib import admin
from .models import Category,Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'category', 'is_active', 'price']
    prepopulated_fields = {'slug': ('name',)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'slug']
    ordering = ['is_featured']
    prepopulated_fields = {'slug': ('name',)}

    def name(self, obj):
        # by returning the object, it displays __str__ method of our obj.
        return obj


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)

