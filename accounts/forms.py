from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomerCreationForm(UserCreationForm):
    first_name = forms.TextInput()
    last_name = forms.TextInput()

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]
        labels = {
            'first_name': '',
            'last_name': '',
            'username': '',
            'email': '',
            'phone': ''
        }
        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control form-control-lg mt-3 mb-3', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control form-control-lg mt-3 mb-3', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(
                attrs={'class': 'form-control mt-3 mb-3', 'placeholder': 'Username'}),
            'email': forms.TextInput(
                attrs={'class': 'form-control form-control-lg mt-3 mb-3', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control mt-3 mb-3', 'placeholder': 'Phone Number'}),

        }

