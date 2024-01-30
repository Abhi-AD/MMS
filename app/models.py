from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

# Create your models here.


class Member(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Customer(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    images = models.ImageField(upload_to="Customer/%Y/%m/%d", blank=False)
    street_address = models.CharField(max_length=255, blank=True, null=True)
    street_address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state_province = models.CharField(max_length=100, blank=True, null=True)
    date_of_signature = models.DateTimeField(default=timezone.now)
    contact = models.CharField(max_length=10)
    emergency_contact = models.CharField(max_length=10, blank=True, null=True)
    emergency_contact2 = models.CharField(max_length=10, blank=True, null=True)
    rollnumber = models.CharField(max_length=20, unique=True, editable=False)

    def __str__(self):
        return (
            f"{self.member.first_name} {self.member.last_name} Rollno:{self.rollnumber}"
        )

    def save(self, *args, **kwargs):
        date_prefix = timezone.now().strftime("%m-%d-%y")
        roll_number = f"{date_prefix}-{self.pk}"
        self.rollnumber = roll_number
        super().save(*args, **kwargs)


class CustomerApplyRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("pending approval", "Pending Approval"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    member = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    images = models.ImageField(upload_to="Customer_form/%Y/%m/%d", blank=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.member.member.first_name} {self.member.member.last_name} - {self.get_status_display()}"


@receiver(post_save, sender=CustomerApplyRequest)
def handle_customer_apply_request(sender, instance, **kwargs):
    # Delete existing instances in other models with the same member
    PendingCustomerRequest.objects.filter(member=instance.member).delete()
    PendingApprovalModel.objects.filter(member=instance.member).delete()
    ApprovedCustomerRequest.objects.filter(member=instance.member).delete()
    RejectedCustomerRequest.objects.filter(member=instance.member).delete()

    # Create new instances based on the current status
    if instance.status == "pending":
        PendingCustomerRequest.objects.create(
            member=instance.member, images=instance.images, status=instance.status
        )
    elif instance.status == "pending approval":
        PendingApprovalModel.objects.create(
            member=instance.member, images=instance.images, status=instance.status
        )
    elif instance.status == "approved":
        ApprovedCustomerRequest.objects.create(
            member=instance.member, images=instance.images, status=instance.status
        )
    elif instance.status == "rejected":
        RejectedCustomerRequest.objects.create(
            member=instance.member, images=instance.images, status=instance.status
        )


class PendingCustomerRequest(models.Model):
    member = models.ForeignKey(Customer, on_delete=models.CASCADE)
    images = models.ImageField(upload_to="PendingCustomerRequest/%Y/%m/%d", blank=True)
    status = models.CharField(
        max_length=20, choices=CustomerApplyRequest.STATUS_CHOICES, default="pending"
    )
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.member.member.first_name} {self.member.member.last_name} - {self.get_status_display()}"


class PendingApprovalModel(models.Model):
    member = models.ForeignKey(Customer, on_delete=models.CASCADE)
    images = models.ImageField(upload_to="PendingApprovalModel/%Y/%m/%d", blank=True)
    status = models.CharField(
        max_length=20, choices=CustomerApplyRequest.STATUS_CHOICES, default="pending"
    )
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.member.member.first_name} {self.member.member.last_name} - {self.get_status_display()}"


class ApprovedCustomerRequest(models.Model):
    member = models.ForeignKey(Customer, on_delete=models.CASCADE)
    images = models.ImageField(upload_to="ApprovedCustomerRequest/%Y/%m/%d", blank=True)
    status = models.CharField(
        max_length=20, choices=CustomerApplyRequest.STATUS_CHOICES, default="pending"
    )
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.member.member.first_name} {self.member.member.last_name} - {self.get_status_display()}"


class RejectedCustomerRequest(models.Model):
    member = models.ForeignKey(Customer, on_delete=models.CASCADE)
    images = models.ImageField(upload_to="RejectedCustomerRequest/%Y/%m/%d", blank=True)
    status = models.CharField(
        max_length=20, choices=CustomerApplyRequest.STATUS_CHOICES, default="pending"
    )
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.member.member.first_name} {self.member.member.last_name} - {self.get_status_display()}"
