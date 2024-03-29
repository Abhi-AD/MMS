# Generated by Django 4.2.5 on 2024-01-31 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_remove_customer_customercode'),
        ('admin_app', '0004_servicepayment_delete_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerServicePayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('bill', models.ImageField(upload_to='ServicePayment/%Y/%m/%d')),
                ('category', models.CharField(max_length=100)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.customer')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='servicepayments', to='admin_app.service')),
            ],
        ),
        migrations.DeleteModel(
            name='ServicePayment',
        ),
    ]
