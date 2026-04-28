"""
Messaging database models for the Student 3 individual element.

This file is the main database design for the messaging feature.  It uses two
models instead of one because a message can be sent to more than one person, but
each recipient still needs their own read/deleted state.  For example, if one
recipient deletes a message it should not disappear for every other recipient.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Message(models.Model):
    """
    Stores the message content itself.

    A Message is created by one sender and can be linked to many recipients.
    The recipient-specific information is stored in MessageRecipientStatus
    below, which acts as the custom through table for the many-to-many relation.
    """

    # Status constants are used instead of writing raw strings throughout the
    # code.  This keeps the code easier to maintain and avoids spelling errors.
    STATUS_DRAFT = 'draft'
    STATUS_SENT = 'sent'

    # Django uses this list to display readable choices in forms/admin.
    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_SENT, 'Sent'),
    ]

    # The sender is a Django User. SET_NULL keeps the message record if a user
    # account is removed, which is safer for message history than deleting it.
    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='sent_messages'
    )

    # A message can have multiple recipients.  The custom through model lets the
    # project store per-recipient fields such as is_read and is_deleted.
    recipients = models.ManyToManyField(
        User,
        related_name='received_messages',
        blank=True,
        through='MessageRecipientStatus'
    )

    # Subject is optional so drafts can be saved before the user finishes them.
    subject = models.CharField(max_length=255, blank=True)

    # Body is also optional for the same reason: a draft may be unfinished.
    body = models.TextField(blank=True)

    # Status controls whether the message belongs in Drafts or Sent.
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_DRAFT)

    # sent_at is only populated when the message is actually sent.
    sent_at = models.DateTimeField(null=True, blank=True)

    # created_at and updated_at are useful for ordering drafts and auditing edits.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # By default, newest sent messages appear first.  Drafts fall back to the
        # created_at value if sent_at is empty.
        ordering = ['-sent_at', '-created_at']

    def __str__(self):
        """Readable label used in Django admin and debug output."""
        return f"{self.subject or '(no subject)'} — {self.sender}"

    def get_recipients_display(self):
        """
        Return a comma-separated list of recipient names.

        This is used by the Sent and Drafts pages so the template does not need
        to contain database logic.  Keeping this here makes the templates cleaner.
        """
        users = self.messagerecipientstatus_set.select_related('user')
        names = []
        for rs in users:
            # Prefer full name when available, otherwise fall back to username.
            name = rs.user.get_full_name() or rs.user.username
            names.append(name)
        return ', '.join(names) if names else '(no recipients)'

    def mark_sent(self):
        """
        Convert a draft into a sent message.

        This small helper prevents repeating the same status/timestamp code in
        the compose and edit_draft views.
        """
        self.status = self.STATUS_SENT
        self.sent_at = timezone.now()
        self.save()


class MessageRecipientStatus(models.Model):
    """
    Links a message to one recipient and stores that recipient's state.

    This is the reason the messaging system works properly for multiple users.
    Each recipient can read, unread, or delete their own copy without changing
    how the message appears for other recipients.
    """

    # The message that this recipient-state row belongs to.
    message = models.ForeignKey(Message, on_delete=models.CASCADE)

    # The recipient user for this specific row.
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # False means the message should show as unread in the recipient's inbox.
    is_read = models.BooleanField(default=False)

    # Soft delete: hides a message for one recipient while keeping the original
    # message available for the sender and any other recipients.
    is_deleted = models.BooleanField(default=False)

    # Timestamp showing when the recipient first read the message.
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        # Prevents duplicate state rows for the same user and message.
        unique_together = ('message', 'user')

    def __str__(self):
        """Readable label for Django admin."""
        return f"{self.user.username} / {self.message.subject}"

    def mark_read(self):
        """
        Mark the message as read for this recipient only.

        The guard avoids unnecessarily updating the database if the message has
        already been read.
        """
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()
