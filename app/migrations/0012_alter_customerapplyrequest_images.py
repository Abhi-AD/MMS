# Generated by Django 4.2.5 on 2024-01-25 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_remove_customer_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerapplyrequest',
            name='images',
            field=models.ImageField(upload_to='Customer_form/%Y/%m/%d'),
        ),
    ]