from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, UsernameField
from base.models import ApplicationUser


class UserCreationForm(BaseUserCreationForm):

    class Meta:
        model = ApplicationUser
        fields = ("username", "email")
        field_classes = {
            'username': UsernameField
        }


__all__ = ['UserCreationForm', ]
