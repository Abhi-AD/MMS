# Generated by Django 4.2.5 on 2024-01-30 05:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0030_delete_employeedetail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='customercode',
        ),
    ]
