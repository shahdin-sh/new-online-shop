# Generated by Django 4.1.4 on 2023-10-03 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='session_token',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
