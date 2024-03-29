# Generated by Django 4.2.5 on 2024-01-25 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_alter_customerapplyrequest_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerapplyrequest',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('pending approval', 'Pending Approval'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20),
        ),
    ]
