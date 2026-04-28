from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Extended profile for each registered user.
    Linked 1-to-1 with Django's built-in User model.
    Fields: name, username, email are on the built-in User model.
    This model adds extra Sky-specific fields.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    job_title = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    slack_handle = models.CharField(max_length=100, blank=True, help_text="e.g. @john.doe")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile: {self.user.username}"

    def get_initials(self):
        """Return initials for avatar display."""
        first = self.user.first_name[:1].upper() if self.user.first_name else ''
        last = self.user.last_name[:1].upper() if self.user.last_name else ''
        return f"{first}{last}" or self.user.username[:2].upper()

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
