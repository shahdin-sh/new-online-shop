from django.contrib import admin
from .models import Blog, Tag, Category

class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'content', 'author']
    prepopulated_fields = {'slug': ('title',)}


class TagsAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

# registering admin sites
admin.site.register(Blog, BlogAdmin)
admin.site.register(Tag, TagsAdmin)
admin.site.register(Category, CategoryAdmin)