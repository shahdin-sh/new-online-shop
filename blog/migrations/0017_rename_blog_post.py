# Generated by Django 4.1.4 on 2023-10-17 14:54

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0016_comment_is_spam'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Blog',
            new_name='Post',
        ),
    ]