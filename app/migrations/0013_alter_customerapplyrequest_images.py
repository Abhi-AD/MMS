# Generated by Django 4.2.5 on 2024-01-25 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_customerapplyrequest_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerapplyrequest',
            name='images',
            field=models.ImageField(blank=True, upload_to='Customer_form/%Y/%m/%d'),
        ),
    ]