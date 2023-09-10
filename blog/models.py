from django.db import models
from ckeditor.fields import RichTextField
from accounts.models import CustomUserModel
from django.utils import timezone

class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = RichTextField()
    # In this model only superusers have the permission to published posts
    author = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, limit_choices_to={'is_superuser': True})
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    modified_data = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)  
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)
    category = models.ManyToManyField('Category', related_name='posts_category', blank=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    # def get_absolute_url(self):
    #     return reverse('blog:post_detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.author}: {self.title}'


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