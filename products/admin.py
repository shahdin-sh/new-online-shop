from django.contrib import admin
from .models import Category,Product, Comment
from .forms import SizeAndColorForm

# Start Inlines
class CommentsInline(admin.TabularInline):
    model = Comment
    readonly_fields = ['content','author', 'parent', 'rating']
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


# End Inlines


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'category', 'is_active', 'is_featured', 'product_price', 'datetime_created']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['-datetime_created']
    form = SizeAndColorForm
    inlines = [
        CommentsInline,
    ]

    def product_price(self, obj):
        return f"{obj.price:,} T"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_or_subcategory', 'parent', 'slug']
    ordering = ['is_featured']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [
        ProductsInline,
    ]

    def category_or_subcategory(self, obj):
        # by returning the object, it displays __str__ method of our obj.
        return obj


class CommentAdmin(admin.ModelAdmin):
    list_display = ['content','author', 'product', 'parent', 'datetime_created', 'is_comment', 'rating']

    def is_comment(self, obj):
        if obj.parent:
            return f'replay of {obj.parent}'
        return 'comment'
 

# registering admin sites
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)