# Generated by Django 4.1.4 on 2023-11-23 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0029_alter_product_banner_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='color',
            field=models.CharField(blank=True, choices=[('LARGE', 'large'), ('MEDIUM', 'medium'), ('SMALL', 'small')], max_length=200),
        ),
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.CharField(blank=True, choices=[('BLACK', 'black'), ('WHITE', 'white'), ('PINK', 'pink')], max_length=200),
        ),
    ]