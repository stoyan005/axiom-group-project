
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

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
        return f"Profile: {self.user.username}"

    def get_initials(self):
        first = self.user.first_name[:1].upper() if self.user.first_name else ''
        last = self.user.last_name[:1].upper() if self.user.last_name else ''
        return f"{first}{last}" or self.user.username[:2].upper()

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
