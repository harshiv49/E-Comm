# Generated by Django 3.2.3 on 2022-07-23 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0009_alter_order_transaction_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(blank=True, default=1658574010.425507, editable=False, max_length=200, null=True),
        ),
    ]