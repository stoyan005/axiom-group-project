from django.shortcuts import render, redirect
from .forms import SignUpForm

# Create your views here.

def home(request):
    return render(request, 'portal/login.html')

