from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Customer(models.Model):
    member = models.OneToOneField(User, on_delete=models.CASCADE)
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
        # Generate roll number based on current date and primary key
        date_prefix = timezone.now().strftime("%m-%d-%y")
        roll_number = f"{date_prefix}-{self.pk}"

        # Assign the generated roll number
        self.rollnumber = roll_number

        # Call the original save method to save the instance
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
    images = models.ImageField(upload_to="Cutomer_form/%Y/%m/%d", blank=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.member.member.first_name} {self.member.member.last_name}"




@receiver(post_save, sender=CustomerApplyRequest)
def handle_customer_apply_request(sender, instance, **kwargs):
    if instance.status == "pending":
        # Save data in PendingCustomerRequest
        PendingCustomerRequest.objects.create(member=instance.member, images=instance.images)
    elif instance.status == "pending approval":
        # Save data in PendingApprovalModel
        PendingApprovalModel.objects.create(
            member=instance.member, images=instance.images
        )
    elif instance.status == "approved":
        # Save data in ApprovedCustomerRequest
        ApprovedCustomerRequest.objects.create(member=instance.member, images=instance.images)
    elif instance.status == "rejected":
        # Save data in RejectedCusomerRequest
        RejectedCusomerRequest.objects.create(member=instance.member, images=instance.images)


class PendingCustomerRequest(models.Model):
    member = models.ForeignKey(Customer, on_delete=models.CASCADE)
    images = models.ImageField(upload_to="PendingCustomerRequest/%Y/%m/%d", blank=True)

    def __str__(self):
        return f"{self.member.member.first_name} {self.member.member.last_name}"


class PendingApprovalModel(models.Model):
    member = models.ForeignKey(Customer, on_delete=models.CASCADE)
    images = models.ImageField(upload_to="PendingApprovalModel/%Y/%m/%d", blank=True)

    def __str__(self):
        return f"{self.member.member.first_name} {self.member.member.last_name}"


class ApprovedCustomerRequest(models.Model):
    member = models.ForeignKey(Customer, on_delete=models.CASCADE)
    images = models.ImageField(upload_to="ApprovedCustomerRequest/%Y/%m/%d", blank=True)

    def __str__(self):
        return f"{self.member.member.first_name} {self.member.member.last_name}"


class RejectedCusomerRequest(models.Model):
    member = models.ForeignKey(Customer, on_delete=models.CASCADE)
    images = models.ImageField(upload_to="RejectedCusomerRequest/%Y/%m/%d", blank=True)

    def __str__(self):
        return f"{self.member.member.first_name} {self.member.member.last_name}"
