# Generated by Django 4.1.4 on 2023-10-03 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='color',
            field=models.CharField(default='black', max_length=200),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='size',
            field=models.CharField(default='large', max_length=200),
        ),
    ]