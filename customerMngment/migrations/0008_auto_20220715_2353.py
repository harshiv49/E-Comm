# Generated by Django 3.2.3 on 2022-07-15 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customerMngment', '0007_customer_order_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.RemoveField(
            model_name='product',
            name='tag',
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
