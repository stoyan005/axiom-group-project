from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Message(models.Model):
    """
    Core message model. Supports inbox, sent, and drafts.
    A message has one sender and many recipients.
    Status: 'draft' = saved but not sent. 'sent' = delivered.
    """
    STATUS_DRAFT = 'draft'
    STATUS_SENT = 'sent'
    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_SENT, 'Sent'),
    ]

    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='sent_messages'
    )
    recipients = models.ManyToManyField(
        User,
        related_name='received_messages',
        blank=True,
        through='MessageRecipientStatus'
    )
    subject = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-sent_at', '-created_at']

    def __str__(self):
        return f"{self.subject or '(no subject)'} — {self.sender}"

    def get_recipients_display(self):
        """Return comma-separated list of recipient full names."""
        users = self.messagerecipientstatus_set.select_related('user')
        names = []
        for rs in users:
            name = rs.user.get_full_name() or rs.user.username
            names.append(name)
        return ', '.join(names) if names else '(no recipients)'

    def mark_sent(self):
        self.status = self.STATUS_SENT
        self.sent_at = timezone.now()
        self.save()


class MessageRecipientStatus(models.Model):
    """
    Through-table linking Message → recipient User.
    Tracks per-user read/deleted state without affecting other recipients.
    """
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('message', 'user')

    def __str__(self):
        return f"{self.user.username} / {self.message.subject}"

    def mark_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()
