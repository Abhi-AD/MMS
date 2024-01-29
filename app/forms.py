from django import forms
from app.models import (
    Customer,
    CustomerApplyRequest
)




class CustomerApplyRequestForm(forms.ModelForm):
    class Meta:
        model = CustomerApplyRequest
        fields = ['images']







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
    


class CustomerProfileEditForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'images',
            'street_address',
            'street_address2',
            'city',
            'state_province',
            'contact',
            'emergency_contact',
            'emergency_contact2',
        ]
