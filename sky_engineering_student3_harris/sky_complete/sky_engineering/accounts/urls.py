
from django.urls import path
from . import views

# app_name gives these routes a namespace, e.g. accounts:profile.
app_name = 'accounts'

urlpatterns = [
    # Local registration page.
    path('register/', views.register, name='register'),

    # Logged-in user's profile page.
    path('profile/', views.profile, name='profile'),

    # Password change page using Django's PasswordChangeForm.
    path('change-password/', views.change_password, name='change_password'),
]
