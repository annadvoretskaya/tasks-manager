from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, UsernameField
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _


class UserCreationForm(BaseUserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        strip=False,
        required=True,
        widget=forms.EmailInput,
    )

    class Meta:
        model = User
        fields = ("username", "email")
        field_classes = {
            'username': UsernameField
        }