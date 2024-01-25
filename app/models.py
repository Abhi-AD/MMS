from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

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

    def __str__(self):
        return f"{self.member.first_name} {self.member.last_name}"
    
    
class CustomerApplyRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ('pending approval', 'Pending Approval'),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    member = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    images = models.ImageField(upload_to="Cutomer_form/%Y/%m/%d", blank=True)
    update_at = models.DateTimeField(auto_now=True)
    

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     # Automatically save or delete AddMember instance based on status
    #     if self.status == "approved" and self.images:
    #         # If status is approved and images are present, do something
    #         # For example, you can access images using self.images
    #         pass
    #     elif self.status == "rejected":
    #         # If status is rejected, delete the associated AddMember instance
    #         self.delete()
    
       
    def __str__(self):
        return f"{self.member.member.first_name} {self.member.member.last_name}"
            
 


          
    