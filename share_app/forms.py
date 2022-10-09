from django import forms
from django.core.exceptions import ValidationError
from .models import User


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)
    email = forms.EmailField()
    password1 = forms.CharField(max_length=128)
    password2 = forms.CharField(max_length=128)

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
