# Generated by Django 4.2.5 on 2024-01-25 07:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_alter_customerapplyrequest_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='email',
            field=models.EmailField(default=datetime.datetime(2024, 1, 25, 7, 16, 29, 517357, tzinfo=datetime.timezone.utc), max_length=254),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customerapplyrequest',
            name='images',
            field=models.ImageField(blank=True, upload_to='Cutomer_form/%Y/%m/%d'),
        ),
    ]
