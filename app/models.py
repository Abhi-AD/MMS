from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class AddMember(models.Model):
    STATUS_PAYMENT = [
        ("online", "Online"),
        ("case", "Case"),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    images = models.ImageField(upload_to="Addmember/%Y/%m/%d", blank=False)
    street_address = models.CharField(max_length=255, blank=True, null=True)
    street_address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state_province = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    billing_address = models.CharField(max_length=20, choices=STATUS_PAYMENT)
    date_of_signature = models.DateTimeField(default=timezone.now)
    contact = models.CharField(max_length=10)
    emergency_contact = models.CharField(max_length=10, blank=True, null=True)
    emergency_contact2 = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
