from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import User


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)
    email = forms.EmailField()
    password1 = forms.CharField(max_length=64)
    password2 = forms.CharField(max_length=64)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise ValidationError('Passwords do not match!')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('User with this login already exists.')
        return email


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=64)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists() is False:
            raise ValidationError('User with this login does not exists.')
        return email

    def clean(self):
        cd = super().clean()
        email = cd.get('email')
        password = cd.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            raise ValidationError("Wrong mail or password!")
