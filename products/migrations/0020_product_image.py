# Generated by Django 4.1.4 on 2023-02-06 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_remove_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default='product_default/shopping_kart.jpg', upload_to='product/'),
        ),
    ]