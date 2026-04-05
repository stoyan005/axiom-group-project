from django import forms
from django.contrib.auth.models import User

class SignUpForm(forms.ModelForm):
    # Custom field not in the default User model
    department = forms.CharField(
        max_length=100, 
        label="Department / Team",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your team'})
    )
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        # Apply CSS classes to match the rounded input style
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control rounded-pill'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control rounded-pill'}),
            'email': forms.EmailInput(attrs={'class': 'form-control rounded-pill'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control rounded-pill'}),
        }