from django.db import models

# Create your models here.
           
class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    bill = models.ImageField(upload_to="Payment/%Y/%m/%d")
    category = models.CharField(max_length=100)  # Corrected typo in max_length

    
    def __str__(self):
        return f"{self.category} {self.amount}"