from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.core.mail import send_mail

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username',]
    