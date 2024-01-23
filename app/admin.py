from django.contrib import admin
from app.models import (
    AddMember,
    RegistrationRequest,
    Payment

)


# Register your models here.
admin.site.register(AddMember)
admin.site.register(RegistrationRequest)
admin.site.register(Payment)
