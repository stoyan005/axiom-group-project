from django.shortcuts import render, redirect
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import RegistrationForm, ProfileUpdateForm, ExtendedProfileForm
from .models import UserProfile


def register(request):
    """
    Self-registration view. Local accounts only.
    Requirement: Users must be able to self-register (no Google ID etc).
    """
    if request.user.is_authenticated:
        return redirect('messaging:inbox')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to Sky Engineering Portal, {user.first_name}!')
            return redirect('messaging:inbox')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    """
    View and update user profile.
    Requirement: Users must be able to update profile, change password if required.
    """
    profile_obj, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = ProfileUpdateForm(request.POST, instance=request.user)
        profile_form = ExtendedProfileForm(request.POST, instance=profile_obj)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
    else:
        user_form = ProfileUpdateForm(instance=request.user)
        profile_form = ExtendedProfileForm(instance=profile_obj)

    return render(request, 'registration/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@login_required
def change_password(request):
    """Allow logged-in users to change their password."""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, 'Password changed successfully.')
            return redirect('accounts:profile')
    else:
        form = PasswordChangeForm(request.user)
        for field in form.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    return render(request, 'registration/change_password.html', {'form': form})
