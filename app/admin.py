from django.contrib import admin
from app.models import (
    AddMember,
    RegistrationRequest,

)


# Register your models here.
admin.site.register(AddMember)
admin.site.register(RegistrationRequest)
