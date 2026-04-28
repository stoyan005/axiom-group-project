"""
Views for the Student 3 messaging module.

Each view handles one browser action, such as opening the inbox, composing a
message, saving a draft, or changing read status.  The @login_required decorator
protects these pages so only authenticated users can access messaging.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import Message, MessageRecipientStatus
from .forms import ComposeMessageForm


@login_required
def inbox(request):
    """Display received sent messages for the logged-in user."""

    # Find all message-state rows that belong to the current user.  The actual
    # Message and sender are selected at the same time to reduce database queries.
    user_statuses = MessageRecipientStatus.objects.filter(
        user=request.user,
        is_deleted=False,
        message__status=Message.STATUS_SENT
    ).select_related('message', 'message__sender').order_by('-message__sent_at')

    # The redesigned UI shows a preview of the newest/selected conversation.
    selected_status = user_statuses[0] if user_statuses else None

    # active_tab is used by the base template to highlight the Messages sidebar item.
    return render(request, 'messaging/inbox.html', {
        'user_statuses': user_statuses,
        'selected_status': selected_status,
        'active_tab': 'inbox',
    })


@login_required
def sent(request):
    """Display messages sent by the logged-in user."""

    # A sent message is one where the current user is the sender and status is sent.
    sent_messages = Message.objects.filter(
        sender=request.user,
        status=Message.STATUS_SENT
    ).order_by('-sent_at')

    return render(request, 'messaging/sent.html', {
        'sent_messages': sent_messages,
        'active_tab': 'sent',
    })


@login_required
def drafts(request):
    """Display draft messages that belong to the logged-in user."""

    # Drafts are ordered by updated_at so recently edited drafts appear first.
    draft_messages = Message.objects.filter(
        sender=request.user,
        status=Message.STATUS_DRAFT
    ).order_by('-updated_at')

    return render(request, 'messaging/drafts.html', {
        'draft_messages': draft_messages,
        'active_tab': 'drafts',
    })


@login_required
def compose(request):
    """Create a new message and either send it or save it as a draft."""

    # Create an empty form for GET requests.  current_user removes the sender
    # from the recipient list.
    form = ComposeMessageForm(current_user=request.user)

    if request.method == 'POST':
        # Bind the submitted data to the form so Django can validate it.
        form = ComposeMessageForm(request.POST, current_user=request.user)
        if form.is_valid():
            # The submit button controls whether the message is sent or drafted.
            action = request.POST.get('action', 'send')

            # commit=False lets us add the sender/status before saving.
            msg = form.save(commit=False)
            msg.sender = request.user

            if action == 'draft':
                # Drafts are stored but not treated as delivered messages yet.
                msg.status = Message.STATUS_DRAFT
                msg.save()

                # Recipients are stored in the through table so their state can
                # be tracked later if the draft is sent.
                for recipient in form.cleaned_data['recipients']:
                    MessageRecipientStatus.objects.get_or_create(
                        message=msg, user=recipient
                    )
                messages.success(request, 'Draft saved.')
                return redirect('messaging:drafts')

            # Sending uses the helper method on the model to set sent_at.
            msg.mark_sent()
            for recipient in form.cleaned_data['recipients']:
                MessageRecipientStatus.objects.get_or_create(
                    message=msg, user=recipient
                )
            messages.success(request, 'Message sent.')
            return redirect('messaging:sent')

    return render(request, 'messaging/compose.html', {
        'form': form,
        'active_tab': 'inbox',
    })


@login_required
def edit_draft(request, message_id):
    """Open an existing draft so the sender can edit or send it."""

    # The lookup confirms the draft belongs to the logged-in user.  This prevents
    # one user from editing another user's draft by changing the URL.
    msg = get_object_or_404(
        Message, pk=message_id, sender=request.user, status=Message.STATUS_DRAFT
    )

    if request.method == 'POST':
        # instance=msg tells Django to update the existing draft instead of
        # creating a completely new message record.
        form = ComposeMessageForm(request.POST, instance=msg, current_user=request.user)
        if form.is_valid():
            action = request.POST.get('action', 'draft')
            updated = form.save(commit=False)
            updated.sender = request.user

            # Remove old recipient rows first so changed recipient selections do
            # not leave stale or duplicate recipients behind.
            MessageRecipientStatus.objects.filter(message=msg).delete()

            if action == 'send':
                updated.mark_sent()
                for recipient in form.cleaned_data['recipients']:
                    MessageRecipientStatus.objects.get_or_create(
                        message=updated, user=recipient
                    )
                messages.success(request, 'Message sent.')
                return redirect('messaging:sent')

            # If the user saves again, keep the message as a draft.
            updated.status = Message.STATUS_DRAFT
            updated.save()
            for recipient in form.cleaned_data['recipients']:
                MessageRecipientStatus.objects.get_or_create(
                    message=updated, user=recipient
                )
            messages.success(request, 'Draft updated.')
            return redirect('messaging:drafts')

    else:
        # On the first page load, pre-select the recipients already attached to
        # this draft so the user can see and edit the existing selection.
        existing_recipients = User.objects.filter(
            messagerecipientstatus__message=msg
        )
        form = ComposeMessageForm(
            instance=msg,
            current_user=request.user,
            initial={'recipients': existing_recipients}
        )

    return render(request, 'messaging/compose.html', {
        'form': form,
        'draft': msg,
        'active_tab': 'drafts',
    })


@login_required
def view_message(request, message_id):
    """Display one message and mark it as read if the viewer is a recipient."""

    msg = get_object_or_404(Message, pk=message_id)

    # Users can only view messages they sent or messages they received.
    is_recipient = MessageRecipientStatus.objects.filter(
        message=msg, user=request.user
    ).exists()
    is_sender = (msg.sender == request.user)

    if not is_recipient and not is_sender:
        # This is the main access-control check for private messages.
        messages.error(request, 'You do not have permission to view this message.')
        return redirect('messaging:inbox')

    if is_recipient:
        # Reading a message automatically updates that user's recipient row.
        status_obj = MessageRecipientStatus.objects.get(message=msg, user=request.user)
        status_obj.mark_read()

    # The side panel needs the inbox list as well as the selected message.
    inbox_statuses = MessageRecipientStatus.objects.filter(
        user=request.user,
        is_deleted=False,
        message__status=Message.STATUS_SENT
    ).select_related('message', 'message__sender').order_by('-message__sent_at')

    return render(request, 'messaging/view_message.html', {
        'message': msg,
        'is_recipient': is_recipient,
        'user_statuses': inbox_statuses,
        'active_tab': 'inbox',
    })


@login_required
def toggle_read(request, message_id):
    """Switch a message between read and unread for the current recipient."""

    # get_object_or_404 ensures the current user is actually a recipient.
    status_obj = get_object_or_404(
        MessageRecipientStatus, message__pk=message_id, user=request.user
    )

    # Flip the boolean value.
    status_obj.is_read = not status_obj.is_read

    # Keep read_at meaningful by clearing it when a message is set back to unread.
    if status_obj.is_read:
        status_obj.read_at = timezone.now()
    else:
        status_obj.read_at = None

    status_obj.save()
    return redirect('messaging:inbox')


@login_required
def delete_message(request, message_id):
    """
    Delete behaviour for the current user.

    Recipients get a soft delete so the message disappears from their inbox only.
    Senders can permanently delete their own sent messages or drafts.
    """

    msg = get_object_or_404(Message, pk=message_id)
    referer = request.META.get('HTTP_REFERER', '')

    # If the logged-in user is a recipient, hide the message for them only.
    status_qs = MessageRecipientStatus.objects.filter(
        message=msg, user=request.user
    )
    if status_qs.exists():
        status_qs.update(is_deleted=True)
        messages.success(request, 'Message removed from inbox.')
        return redirect('messaging:inbox')

    # If the logged-in user is the sender, remove the message record itself.
    if msg.sender == request.user:
        msg.delete()
        messages.success(request, 'Message deleted.')
        if 'sent' in referer:
            return redirect('messaging:sent')
        return redirect('messaging:drafts')

    # If neither condition is true, the user has no permission to delete it.
    messages.error(request, 'You cannot delete this message.')
    return redirect('messaging:inbox')


@login_required
def unread_count_api(request):
    """Return the unread count as JSON for future dynamic navbar updates."""

    count = MessageRecipientStatus.objects.filter(
        user=request.user,
        is_read=False,
        is_deleted=False,
        message__status=Message.STATUS_SENT
    ).count()
    return JsonResponse({'unread_count': count})
