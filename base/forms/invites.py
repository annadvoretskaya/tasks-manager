from django import forms
from base.models import Invite


class InviteForm(forms.ModelForm):
    class Meta:
        model = Invite
        fields = ('email', )