# Generated by Django 4.1.4 on 2023-07-24 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_rename_name_order_first_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='area',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
