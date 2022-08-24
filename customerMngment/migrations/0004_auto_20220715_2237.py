# Generated by Django 3.2.3 on 2022-07-15 17:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customerMngment', '0003_auto_20220712_2019'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='phome',
            new_name='phone',
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
