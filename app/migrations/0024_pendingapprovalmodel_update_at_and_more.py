# Generated by Django 4.2.5 on 2024-01-28 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_alter_pendingapprovalmodel_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pendingapprovalmodel',
            name='update_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='pendingcustomerrequest',
            name='update_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='rejectedcustomerrequest',
            name='update_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]