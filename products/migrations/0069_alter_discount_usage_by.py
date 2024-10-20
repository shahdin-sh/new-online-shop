# Generated by Django 4.1.4 on 2024-03-10 16:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0068_remove_discount_session_restore_discount_usage_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='usage_by',
            field=models.ManyToManyField(blank=True, related_name='applied_discount', to=settings.AUTH_USER_MODEL),
        ),
    ]