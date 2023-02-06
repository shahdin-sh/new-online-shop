from django.db import models
from django.shortcuts import reverse


class Category(models.Model):
    # Category_Choices = (
    #     ('NONE CATEGORY', 'none category'),
    #     ('HOME AND KITCHEN', 'home and kitchen'),
    #     ('SPORT', 'sport'),
    #     ('LOCAL PRODUCTS', 'local products'),
    #     ('TOYS', 'toys'),
    #     ('COMMODITY', 'commodity'),
    #     ('FASHION AND CLOTHING', 'fashion and clothing'),
    #     ('TOOLS AND EQUIPMENT', 'tools and equipment'),
    #     ('DIGITAL COMMODITY', 'digital commodity')
    # )
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    is_featured = models.BooleanField(null=True)
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
    description = models.TextField()
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
