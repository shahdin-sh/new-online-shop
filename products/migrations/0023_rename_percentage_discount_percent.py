# Generated by Django 4.1.4 on 2023-11-05 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_discount_percentage_alter_discount_value'),
    ]

    operations = [
        migrations.RenameField(
            model_name='discount',
            old_name='percentage',
            new_name='percent',
        ),
    ]