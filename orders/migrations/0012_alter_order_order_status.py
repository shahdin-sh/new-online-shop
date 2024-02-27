# Generated by Django 4.1.4 on 2023-12-27 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_alter_order_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('Paid', 'PAID'), ('Unpaid', 'UNPAID'), ('Canceled', 'CANCELED')], default='Unpaid', max_length=100),
        ),
    ]