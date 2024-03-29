from django.db import models
from django.utils import timezone
from app.models import Customer

# Create your models here.


class Service(models.Model):
    SERVICE_CATEGORIES = [
        ("Training", "Training"),
        ("Membership", "Membership"),
        ("Tickets", "Tickets"),
    ]

    name = models.CharField(max_length=255, verbose_name="Service/Product")
    images = models.ImageField(upload_to="Service/Product/%Y/%m/%d", blank=False)
    duration_days = models.IntegerField(verbose_name="Day/Session")
    category = models.CharField(
        max_length=20, choices=SERVICE_CATEGORIES, verbose_name="Service Category"
    )
    non_refundable_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Non-refundable"
    )
    refundable_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Refundable",
        null=True,
        blank=True,
    )
    basis_foundation = models.CharField(
        max_length=50, verbose_name="Basis/foundation", null=True, blank=True
    )
    emi_available = models.BooleanField(default=False, verbose_name="0% EMI Available")
    footfalls = models.IntegerField(
        null=True, blank=True, help_text="Applicable only for Tickets category"
    )
    footfalls_description = models.CharField(max_length=255, null=True, blank=True)
    date_of_signature = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class CustomerServicePayment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    bill = models.ImageField(upload_to="ServicePayment/%Y/%m/%d")
    category = models.CharField(max_length=100)
    
    # ForeignKey to establish a relationship with Service model
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='servicepayments')
    member = models.ForeignKey(Customer, on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.category} {self.amount} for {self.service.name}"










