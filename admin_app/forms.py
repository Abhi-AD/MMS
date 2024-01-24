from django import forms
from admin_app.models import *


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = "__all__"
