# Generated by Django 4.1.4 on 2023-01-31 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_category_category_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='parent',
            new_name='category',
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('slug', 'category')},
        ),
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(blank=True, choices=[('HOME AND KITCHEN', 'home and kitchen'), ('SPORT', 'sport'), ('LOCAL PRODUCTS', 'local products'), ('TOYS', 'toys'), ('COMMODITY', 'commodity'), ('FASHION AND CLOTHING', 'fashion and clothing'), ('TOOLS AND EQUIPMENT', 'tools and equipment'), ('DIGITAL COMMODITY', 'digital commodity')], max_length=200, null=True),
        ),
    ]