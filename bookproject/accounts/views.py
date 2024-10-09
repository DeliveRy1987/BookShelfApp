from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import CreateView

from .forms import SignUpForm

from django.core.mail import send_mail
from django.conf import settings


class SignUpView(CreateView):
    template_name = 'accounts/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('index')
    model = User
    
    
