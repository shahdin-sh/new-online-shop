# Generated by Django 4.1.4 on 2023-01-29 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='product_default/shopping_kart.jpj', upload_to='product/'),
        ),
    ]
