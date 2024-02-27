# Generated by Django 4.1.4 on 2024-01-28 16:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0045_product_datetime_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='selected_product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='products.product'),
        ),
    ]