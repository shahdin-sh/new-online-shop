from typing import Any
from django.contrib import admin
from blog.models import Post, Tag, Category, Comment
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin


class CommentInline(admin.TabularInline):
    model = Comment
    readonly_fields = ['content','author', 'timestamp']
    extra = 1
    classes = ('collapse',)
    can_delete = False
    show_change_link = True


class PostAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['title', 'slug', 'published_date_to_jalali',  'get_content_summary', 'author', 'is_published', 'datetime_created_to_jalali', 'datetime_modified_to_jalali']
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request , obj: Post, form, change):
        if obj.published_date:
            obj.is_published = True
        obj.save()

    @admin.display(description='jalali published_date')
    def published_date_to_jalali(self, obj):
        return datetime2jalali(obj.published_date).strftime('%a, %d %b %Y %H:%M:%S')

    @admin.display(description='jalali datetime_created')
    def datetime_created_to_jalali(self, obj):
        return datetime2jalali(obj.datetime_created).strftime('%a, %d %b %Y %H:%M:%S')
    
    @admin.display(description='jalali datetime_modified')
    def datetime_modified_to_jalali(self, obj):
        return datetime2jalali(obj.datetime_modified).strftime('%a, %d %b %Y %H:%M:%S')


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
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag, TagsAdmin)
admin.site.register(Category, CategoryAdmin)
