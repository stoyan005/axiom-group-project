"""
Signals for automatically maintaining UserProfile rows.

Signals run in response to model events.  Here, whenever a Django User is created,
a matching UserProfile is created automatically so profile pages do not fail.
"""

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile when a new User account is created."""
    if created:
        # get_or_create is defensive: it avoids duplicates if another part of the
        # code has already created the profile.
        UserProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the linked profile whenever the User is saved."""
    if hasattr(instance, 'profile'):
        instance.profile.save()
