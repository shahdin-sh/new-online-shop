# Generated by Django 4.1.4 on 2023-10-26 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_rename_discount_type_discount_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='promo_code',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
