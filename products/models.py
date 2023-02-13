from django.db import models
from django.shortcuts import reverse
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    is_featured = models.BooleanField(null=True, default=False)
    # it determines the subcategory (children) of the category (parent)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    class Meta:
        # enforcing that there can not be two categories under a parent with same slug
        # __str__ method elaborated later in post.  use __unicode__ in place of
        # __str__ if you are using python 2

        unique_together = ('slug', 'parent',)
        verbose_name_plural = "categories"

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        # it means the main category have subcategory and that subcategory could have sub subcategory
        while k is not None:
            # k.name = self.parent.name
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])


class Product(models.Model):

    PRODUCT_QUALITY_CHOICES = (
        ('PERFECT', 'perfect'),
        ('GOOD', 'good'),
        ('NOT BAD', 'not bad'),
        ('BAD', 'bad'),
        ('VERY BAD', 'very bad')
    )

    name = models.CharField(max_length=200)
    description = RichTextField()
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    price = models.PositiveIntegerField()
    slug = models.SlugField(unique=True)
    quality = models.CharField(choices=PRODUCT_QUALITY_CHOICES, max_length=200)
    # problem with this default property
    image = models.ImageField(upload_to='product/', default='product_default/shopping_kart.jpg')

    # add choices
    color = models.CharField(max_length=200, default='black', null=True, blank=True)
    size = models.CharField(max_length=200, null=True, blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    material = models.CharField(max_length=300, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='products')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail_view', args=[self.pk])


class Comments(models.Model):
    content = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    # author here is just users who signed in before! (authenticated users)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self' , null=True , blank=True , on_delete=models.CASCADE , related_name='replies')
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} for {self.product}'

    @property
    def children(self):
        return Comment.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False


