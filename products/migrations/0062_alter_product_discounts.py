# Generated by Django 4.1.4 on 2024-02-19 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0061_alter_discount_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discounts',
            field=models.ManyToManyField(blank=True, related_name='products', to='products.discount'),
        ),
    ]