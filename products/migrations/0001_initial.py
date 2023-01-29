# Generated by Django 4.1.4 on 2023-01-29 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('NONE CATEGORY', 'none category'), ('HOME AND KITCHEN', 'home and kitchen'), ('SPORT', 'sport'), ('LOCAL PRODUCTS', 'local products'), ('TOYS', 'toys'), ('COMMODITY', 'commodity'), ('FASHION AND CLOTHING', 'fashion and clothing'), ('TOOLS AND EQUIPMENT', 'tools and equipment'), ('DIGITAL COMMODITY', 'digital commodity')], max_length=20)),
                ('slug', models.SlugField()),
                ('category_description', models.TextField(blank=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='products.category')),
            ],
            options={
                'verbose_name_plural': 'categories',
                'unique_together': {('slug', 'parent')},
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('quantity', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('price', models.PositiveIntegerField()),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('material', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
                ('quality', models.CharField(choices=[('1', 'perfect'), ('2', 'good'), ('3', 'not bad'), ('4', 'bad'), ('5', 'very bad')], max_length=5)),
                ('image', models.ImageField(default='product_default/', upload_to='product/')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.category')),
            ],
        ),
    ]
