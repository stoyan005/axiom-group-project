"""
Account profile model for the Sky Engineering Portal.

Django already provides the main User model with username, password, first name,
last name and email.  This file adds a small UserProfile model for extra Sky
specific fields without modifying Django's built-in auth model.
"""

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Extra information linked to one Django User account.

    A OneToOneField means each User has one matching profile.  This keeps login
    and password handling inside Django's secure auth system while still giving
    the project space to store job title, department and Slack handle.
    """

    # related_name='profile' lets the code access a profile through user.profile.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # These fields are optional so users can register first and complete profile
    # details later from the profile page.
    job_title = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    slack_handle = models.CharField(max_length=100, blank=True, help_text="e.g. @john.doe")

    # Timestamps provide simple audit information for when a profile was created
    # and last updated.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Readable text shown in Django admin."""
        return f"Profile: {self.user.username}"

    def get_initials(self):
        """
        Return initials for avatar placeholders.

        If the user has not entered first/last names, the username is used as a
        sensible fallback so the UI still has something to display.
        """
        first = self.user.first_name[:1].upper() if self.user.first_name else ''
        last = self.user.last_name[:1].upper() if self.user.last_name else ''
        return f"{first}{last}" or self.user.username[:2].upper()

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
