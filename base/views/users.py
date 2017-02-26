from django.views.generic import CreateView
from base.forms.users import UserCreationForm


class SignUpView(CreateView):
    template_name = 'registration/signup.html'
    form_class = UserCreationForm
    success_url = '/login'
