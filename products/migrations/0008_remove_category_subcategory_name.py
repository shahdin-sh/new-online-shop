# Generated by Django 4.1.4 on 2023-01-31 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_rename_parent_category_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='subcategory_name',
        ),
    ]