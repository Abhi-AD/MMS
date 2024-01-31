from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from admin_app.models import *
from app.models import *


class SuperuserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "is_staff",
            "is_superuser",
            "is_active",
            "first_name",
            "last_name",
        ]


class PaymentForm(forms.ModelForm):
    class Meta:
        model = CustomerServicePayment
        fields = "__all__"


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = [
            "name",
            "images",
            "duration_days",
            "category",
            "non_refundable_price",
            "refundable_price",
            "basis_foundation",
            "emi_available",
            "footfalls",
            "footfalls_description",
        ]


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RequestRegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomerApplyRequest
        fields = ["status"]


class CustomerApplyRequestForm(forms.ModelForm):
    class Meta:
        model = CustomerApplyRequest
        fields = ["status"]
