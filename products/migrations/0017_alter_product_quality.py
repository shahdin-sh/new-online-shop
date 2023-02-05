# Generated by Django 4.1.4 on 2023-02-05 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='quality',
            field=models.CharField(choices=[('PERFECT', 'perfect'), ('GOOD', 'good'), ('NOT BAD', 'not bad'), ('BAD', 'bad'), ('VERY BAD', 'very bad')], max_length=200),
        ),
    ]
