# Generated by Django 4.1.4 on 2023-01-29 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_category_name_alter_product_material_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='media/product_default/shopping_kart.jpj', upload_to='product/'),
        ),
    ]
