# Generated by Django 4.1.4 on 2023-02-16 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0027_remove_comments_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='rating',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
