# Generated by Django 4.1.4 on 2023-07-24 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='name',
            new_name='first_name',
        ),
    ]
