from django import forms
from admin_app.models import *
from app.models import *



class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = "__all__"


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class RequestRegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomerApplyRequest
        fields = ['status']

class CustomerApplyRequestForm(forms.ModelForm):
    class Meta:
        model = CustomerApplyRequest
        fields = ['status']