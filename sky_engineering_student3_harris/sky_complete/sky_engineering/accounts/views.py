
from django.shortcuts import render, redirect
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import RegistrationForm, ProfileUpdateForm, ExtendedProfileForm
from .models import UserProfile


def register(request):

    # If someone is already logged in, send them straight to the main app.
    if request.user.is_authenticated:
        return redirect('messaging:inbox')

    if request.method == 'POST':
        # Bind the submitted form data and let Django validate it.
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Save the user, then immediately log them in for a smooth flow.
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to Sky Engineering Portal, {user.first_name}!')
            return redirect('messaging:inbox')
    else:
        # Empty form for first page load.
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):

    # Make sure every user always has a linked profile record.
    profile_obj, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Two forms are used because some fields live on User and some live on
        # UserProfile.  Both must be valid before anything is saved.
        user_form = ProfileUpdateForm(request.POST, instance=request.user)
        profile_form = ExtendedProfileForm(request.POST, instance=profile_obj)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
    else:
        # Populate both forms with the current database values.
        user_form = ProfileUpdateForm(instance=request.user)
        profile_form = ExtendedProfileForm(instance=profile_obj)

    return render(request, 'registration/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@login_required
def change_password(request):

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
    else:
        form = PasswordChangeForm(request.user)

    # Add Bootstrap styling and helpful placeholders to Django's password form.
    placeholders = {
        'old_password': 'Enter current password',
        'new_password1': 'Enter new password',
        'new_password2': 'Re-enter new password',
    }
    for name, field in form.fields.items():
        field.widget.attrs.update({
            'class': 'form-control',
            'placeholder': placeholders.get(name, field.label),
        })

    if request.method == 'POST' and form.is_valid():
        # PasswordChangeForm saves the new password using Django's password hashing.
        user = form.save()
        # Without this line Django would log the user out after password change.
        update_session_auth_hash(request, user)
        messages.success(request, 'Password changed successfully.')
        return redirect('accounts:profile')

    return render(request, 'registration/change_password.html', {'form': form})
