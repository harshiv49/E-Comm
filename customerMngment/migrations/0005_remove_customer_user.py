# Generated by Django 3.2.3 on 2022-07-15 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customerMngment', '0004_auto_20220715_2237'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='user',
        ),
    ]
