from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from accounts.models import CustomUserModel
from ckeditor.fields import RichTextField


# managers
class IsPublishedManager(models.Manager):
    
    def get_queryset(self):
        return super(IsPublishedManager, self).get_queryset().filter(is_published=True)        


class IsNotSpamManager(models.Manager):
    
    def get_queryset(self):
        return super(IsNotSpamManager, self).get_queryset().filter(is_spam=False)


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = RichTextField()
    # In this model only superusers have the permission to published posts
    author = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, limit_choices_to={'is_superuser': True})
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    datetime_created = models.DateTimeField(auto_now=True)
    datetime_modified = models.DateTimeField(auto_now_add=True)
    list_view_image = models.ImageField(upload_to='blog_images/', blank=True, null=True, default='media\blog_images\1-570x370.webp')
    detail_view_image = models.ImageField(upload_to='blog_images/', blank=True, null=True, default='media\blog_images\1-870x500.webp')
    small_detail_view_image = models.ImageField(upload_to='blog_images/', blank=True, null=True, default='media\blog_images\1-420x241.webp') 
    small_detail_view_image_2 = models.ImageField(upload_to='blog_images/', blank=True, null=True, default='media\blog_images\1-420x241.webp')           
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)
    category = models.ForeignKey('Category', related_name='posts', blank=True, null=True, on_delete=models.CASCADE)

    # Custom Managers
    objects = models.Manager()
    is_published_manager = IsPublishedManager()


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[str(self.slug)])

    def __str__(self):
        return f'{self.author}: {self.title}'
    

    def get_content_summary(self):
        content = strip_tags(self.content)
        return content[:70] 


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    content = RichTextField()
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='post_comments')
    timestamp = models.DateTimeField(auto_now_add=True)
    is_spam = models.BooleanField(default=False)

    # Custom Managers
    objects = models.Manager()
    is_not_spam_manager = IsNotSpamManager()


    def __str__(self):
        return f"{self.author}'s comment, id:{self.id}"
    

    def get_absolute_url(self):
        return reverse('blog:comment_detail', args=[str(self.slug)])
    
    
    def get_content_summary(self):
        content = strip_tags(self.content)
        return content[:30] 
