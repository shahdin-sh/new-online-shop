# Generated by Django 4.1.4 on 2023-12-26 17:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_alter_customerwithaddress_country_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerwithaddress',
            name='area',
        ),
    ]
