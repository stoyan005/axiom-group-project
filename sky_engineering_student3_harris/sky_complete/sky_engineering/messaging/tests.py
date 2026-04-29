
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Message, MessageRecipientStatus


class MessagingWorkflowTests(TestCase):

    def setUp(self):
        self.sender = User.objects.create_user(
            username='sender',
            password='Password123!',
            first_name='Sender',
            last_name='User',
        )
        self.recipient = User.objects.create_user(
            username='recipient',
            password='Password123!',
            first_name='Recipient',
            last_name='User',
        )
        self.other = User.objects.create_user(
            username='other',
            password='Password123!',
        )

    def test_send_message_creates_recipient_status(self):
        self.client.login(username='sender', password='Password123!')
        response = self.client.post(reverse('messaging:compose'), {
            'recipients': [self.recipient.id],
            'subject': 'Project update',
            'body': 'Please check the latest project update.',
            'action': 'send',
        })

        # The user should be redirected to Sent after sending.
        self.assertRedirects(response, reverse('messaging:sent'))

        message = Message.objects.get(subject='Project update')
        self.assertEqual(message.status, Message.STATUS_SENT)
        self.assertEqual(message.sender, self.sender)
        self.assertTrue(
            MessageRecipientStatus.objects.filter(message=message, user=self.recipient).exists()
        )

    def test_save_draft_and_send_later(self):
        self.client.login(username='sender', password='Password123!')
        response = self.client.post(reverse('messaging:compose'), {
            'recipients': [self.recipient.id],
            'subject': 'Draft Plan',
            'body': 'Initial draft text.',
            'action': 'draft',
        })
        self.assertRedirects(response, reverse('messaging:drafts'))

        draft = Message.objects.get(subject='Draft Plan')
        self.assertEqual(draft.status, Message.STATUS_DRAFT)

        # Reopen the same draft and submit it with action=send.
        response = self.client.post(reverse('messaging:edit_draft', args=[draft.id]), {
            'recipients': [self.recipient.id],
            'subject': 'Draft Plan Final',
            'body': 'Final message text.',
            'action': 'send',
        })
        self.assertRedirects(response, reverse('messaging:sent'))

        draft.refresh_from_db()
        self.assertEqual(draft.status, Message.STATUS_SENT)
        self.assertEqual(draft.subject, 'Draft Plan Final')

    def test_inbox_marks_message_as_read_when_viewed(self):
        message = Message.objects.create(
            sender=self.sender,
            subject='Read test',
            body='Open this message.',
            status=Message.STATUS_SENT,
        )
        status = MessageRecipientStatus.objects.create(message=message, user=self.recipient)

        self.client.login(username='recipient', password='Password123!')
        response = self.client.get(reverse('messaging:view_message', args=[message.id]))

        self.assertEqual(response.status_code, 200)
        status.refresh_from_db()
        self.assertTrue(status.is_read)
        self.assertIsNotNone(status.read_at)

    def test_toggle_read_changes_read_state(self):
        message = Message.objects.create(
            sender=self.sender,
            subject='Toggle test',
            body='Toggle this message.',
            status=Message.STATUS_SENT,
        )
        status = MessageRecipientStatus.objects.create(
            message=message,
            user=self.recipient,
            is_read=True,
        )

        self.client.login(username='recipient', password='Password123!')
        response = self.client.get(reverse('messaging:toggle_read', args=[message.id]))

        self.assertRedirects(response, reverse('messaging:inbox'))
        status.refresh_from_db()
        self.assertFalse(status.is_read)

    def test_unauthorised_user_cannot_view_private_message(self):
        message = Message.objects.create(
            sender=self.sender,
            subject='Private',
            body='This should not be visible to another user.',
            status=Message.STATUS_SENT,
        )
        MessageRecipientStatus.objects.create(message=message, user=self.recipient)

        self.client.login(username='other', password='Password123!')
        response = self.client.get(reverse('messaging:view_message', args=[message.id]))

        self.assertRedirects(response, reverse('messaging:inbox'))
