from django.contrib import admin
from app.models import (
    Customer,
    CustomerApplyRequest,

)


# Register your models here.
admin.site.register(Customer)
admin.site.register(CustomerApplyRequest)
