from typing import Any
from django.contrib import admin
from .models import Blog, Tag, Category, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    readonly_fields = ['content','author', 'timestamp']
    extra = 1
    classes = ('collapse',)
    can_delete = False
    show_change_link = True


class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'published_date',  'get_content_summary', 'author', 'is_published']
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request , obj: Blog, form, change):
        if obj.published_date:
            obj.is_published = True
        obj.save()

    inlines = [
        CommentInline
    ]

class CommentAdmin(admin.ModelAdmin):
    list_display = ['get_content_summary', 'author', 'timestamp', 'is_spam']


class TagsAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

# registering admin sites
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag, TagsAdmin)
admin.site.register(Category, CategoryAdmin)
