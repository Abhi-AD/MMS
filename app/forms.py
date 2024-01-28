from django import forms
from app.models import (
    Customer,
    CustomerApplyRequest
)

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomerApplyRequest
        fields = ["member", "images"]



class UserRegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)





class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))





class CustomerRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    customercode = forms.IntegerField()
    username = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    images = forms.FileField() 
    
