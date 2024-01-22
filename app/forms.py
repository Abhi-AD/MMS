from django import forms
from app.models import (
    AddMember,
)


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = AddMember
        fields = "__all__"
