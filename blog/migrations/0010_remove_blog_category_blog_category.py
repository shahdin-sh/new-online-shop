# Generated by Django 4.1.4 on 2023-09-23 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_blog_small_detail_view_image_2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='category',
        ),
        migrations.AddField(
            model_name='blog',
            name='category',
            field=models.ManyToManyField(blank=True, null=True, related_name='posts_category', to='blog.category'),
        ),
    ]
