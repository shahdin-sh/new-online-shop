# Generated by Django 4.1.4 on 2023-02-13 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
