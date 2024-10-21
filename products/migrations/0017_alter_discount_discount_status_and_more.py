# Generated by Django 4.1.4 on 2023-10-26 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_alter_discount_discount_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='discount_status',
            field=models.CharField(choices=[('AC', 'ACTIVE'), ('DC', 'DEACTIVE')], default='AC', max_length=255),
        ),
        migrations.AlterField(
            model_name='discount',
            name='discount_type',
            field=models.CharField(choices=[('PD', 'PERCENTAGE DISCOUNT'), ('FAD', 'FIXED AMOUNT DISCOUNT'), ('BOGO', 'BUY ONE GET ONE')], max_length=255),
        ),
        migrations.AlterField(
            model_name='discount',
            name='promo_code',
            field=models.CharField(blank=True, max_length=255, unique=True),
        ),
    ]