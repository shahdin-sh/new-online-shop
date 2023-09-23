from typing import Any
from django.contrib import admin
from .models import Blog, Tag, Category

class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'published_date',  'get_content_summary', 'author', 'is_published']
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request , obj: Blog, form, change):
        if obj.published_date:
            obj.is_published = True
        obj.save()


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