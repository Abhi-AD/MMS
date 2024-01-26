from django.contrib import admin
from app.models import (
    Customer,
    CustomerApplyRequest,
    PendingCustomerRequest,
    PendingApprovalModel,
    ApprovedCustomerRequest,
    RejectedCusomerRequest,

)


# Register your models here.
admin.site.register(Customer)
admin.site.register(CustomerApplyRequest)
admin.site.register(PendingCustomerRequest)
admin.site.register(PendingApprovalModel)
admin.site.register(ApprovedCustomerRequest)
admin.site.register(RejectedCusomerRequest)