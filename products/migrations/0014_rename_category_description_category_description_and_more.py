# Generated by Django 4.1.4 on 2023-02-04 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_alter_category_category_name_alter_product_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='category_description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='category_name',
            new_name='name',
        ),
    ]