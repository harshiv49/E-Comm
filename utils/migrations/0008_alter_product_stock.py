# Generated by Django 3.2.3 on 2022-07-17 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0007_order_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]