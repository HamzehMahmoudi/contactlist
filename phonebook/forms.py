from django import forms
from .models import PhoneBook
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class NewContactForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=11, required=True)

    class Meta:
        model = PhoneBook
        fields = [
            "first_name",
            "last_name",
            "phone_number",
        ]
        exclude = ["user"]


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2")
