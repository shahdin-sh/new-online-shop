from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + str(self.category)


class Product(models.Model):

    PRODUCT_QUALITY_CHOICES = (
        ('1', 'perfect'),
        ("2", 'good'),
        ('3', 'not bad'),
        ("4", 'bad'),
        ("5", 'very bad')
    )

    name = models.CharField(max_length=20)
    description = models.TextField()
    quantity = models.IntegerField()
    price = models.PositiveIntegerField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    material = models.CharField(max_length=50)
    category = models.OneToOneField(Category, on_delete=models.CASCADE)
    sub_category = models.OneToOneField(SubCategory, on_delete=models.CASCADE)
    quality = models.CharField(choices=PRODUCT_QUALITY_CHOICES, max_length=len(PRODUCT_QUALITY_CHOICES))
    image = models.ImageField(upload_to='product/', default='product_default/')

    def __str__(self):
        return self.name
