# Generated by Django 4.2.5 on 2024-01-25 05:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0009_delete_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(upload_to='Customer/%Y/%m/%d')),
                ('street_address', models.CharField(blank=True, max_length=255, null=True)),
                ('street_address2', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state_province', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('date_of_signature', models.DateTimeField(default=django.utils.timezone.now)),
                ('contact', models.CharField(max_length=10)),
                ('emergency_contact', models.CharField(blank=True, max_length=10, null=True)),
                ('emergency_contact2', models.CharField(blank=True, max_length=10, null=True)),
                ('member', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerApplyRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('images', models.ImageField(blank=True, upload_to='Cutomer_form/%Y/%m/%d')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.customer')),
            ],
        ),
        migrations.RemoveField(
            model_name='registrationrequest',
            name='member',
        ),
        migrations.DeleteModel(
            name='AddMember',
        ),
        migrations.DeleteModel(
            name='RegistrationRequest',
        ),
    ]
