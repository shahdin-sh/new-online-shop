from django.db import models
from ckeditor.fields import RichTextField
from accounts.models import CustomUserModel
from django.utils import timezone
from django.utils.html import strip_tags


# managers
class IsPublishedManager(models.Manager):
    
    def get_queryset(self):
        return super(IsPublishedManager, self).get_queryset().filter(is_published=True)           


class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = RichTextField()
    # In this model only superusers have the permission to published posts
    author = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, limit_choices_to={'is_superuser': True})
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    modified_data = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True, default='media\blog_images\1-570x370.webp')  
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)
    category = models.ManyToManyField('Category', related_name='posts_category', blank=True)

    # Custom Managers
    objects = models.Manager()
    is_published_manager = IsPublishedManager()


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    # def get_absolute_url(self):
    #     return reverse('blog:post_detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.author}: {self.title}'
    

    def get_content_summary(self):
        content = strip_tags(self.content)
        return content


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