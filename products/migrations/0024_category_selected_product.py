# Generated by Django 4.1.4 on 2023-11-10 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0023_rename_percentage_discount_percent'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='selected_product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='products.product'),
        ),
    ]
