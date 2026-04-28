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
    """Show all received sent messages for the logged-in user, newest first."""
    user_statuses = MessageRecipientStatus.objects.filter(
        user=request.user,
        is_deleted=False,
        message__status=Message.STATUS_SENT
    ).select_related('message', 'message__sender').order_by('-message__sent_at')

    selected_status = user_statuses[0] if user_statuses else None

    return render(request, 'messaging/inbox.html', {
        'user_statuses': user_statuses,
        'selected_status': selected_status,
        'active_tab': 'inbox',
    })


@login_required
def sent(request):
    """Show all messages sent by the logged-in user."""
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
    """Show all draft messages belonging to the logged-in user."""
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
    """Compose and send a new message, or save as draft."""
    form = ComposeMessageForm(current_user=request.user)

    if request.method == 'POST':
        form = ComposeMessageForm(request.POST, current_user=request.user)
        if form.is_valid():
            action = request.POST.get('action', 'send')
            msg = form.save(commit=False)
            msg.sender = request.user

            if action == 'draft':
                msg.status = Message.STATUS_DRAFT
                msg.save()
                # Save recipients via through-table
                for recipient in form.cleaned_data['recipients']:
                    MessageRecipientStatus.objects.get_or_create(
                        message=msg, user=recipient
                    )
                messages.success(request, 'Draft saved.')
                return redirect('messaging:drafts')
            else:
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
    """Edit an existing draft message."""
    msg = get_object_or_404(
        Message, pk=message_id, sender=request.user, status=Message.STATUS_DRAFT
    )

    if request.method == 'POST':
        form = ComposeMessageForm(request.POST, instance=msg, current_user=request.user)
        if form.is_valid():
            action = request.POST.get('action', 'draft')
            updated = form.save(commit=False)
            updated.sender = request.user

            # Clear old recipients and re-add
            MessageRecipientStatus.objects.filter(message=msg).delete()

            if action == 'send':
                updated.mark_sent()
                for recipient in form.cleaned_data['recipients']:
                    MessageRecipientStatus.objects.get_or_create(
                        message=updated, user=recipient
                    )
                messages.success(request, 'Message sent.')
                return redirect('messaging:sent')
            else:
                updated.status = Message.STATUS_DRAFT
                updated.save()
                for recipient in form.cleaned_data['recipients']:
                    MessageRecipientStatus.objects.get_or_create(
                        message=updated, user=recipient
                    )
                messages.success(request, 'Draft updated.')
                return redirect('messaging:drafts')
    else:
        # Pre-populate recipients from existing through-table rows
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
    """View a single message. Marks as read if the viewer is a recipient."""
    msg = get_object_or_404(Message, pk=message_id)

    # Only sender or recipients may view
    is_recipient = MessageRecipientStatus.objects.filter(
        message=msg, user=request.user
    ).exists()
    is_sender = (msg.sender == request.user)

    if not is_recipient and not is_sender:
        messages.error(request, 'You do not have permission to view this message.')
        return redirect('messaging:inbox')

    # Auto-mark as read for recipients
    if is_recipient:
        status_obj = MessageRecipientStatus.objects.get(message=msg, user=request.user)
        status_obj.mark_read()

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
    """Toggle read/unread for a recipient."""
    status_obj = get_object_or_404(
        MessageRecipientStatus, message__pk=message_id, user=request.user
    )
    status_obj.is_read = not status_obj.is_read
    if status_obj.is_read:
        status_obj.read_at = timezone.now()
    else:
        status_obj.read_at = None
    status_obj.save()
    return redirect('messaging:inbox')


@login_required
def delete_message(request, message_id):
    """
    Soft-delete for recipients (marks is_deleted=True).
    Hard-delete for sender's drafts/sent.
    """
    msg = get_object_or_404(Message, pk=message_id)
    referer = request.META.get('HTTP_REFERER', '')

    status_qs = MessageRecipientStatus.objects.filter(
        message=msg, user=request.user
    )
    if status_qs.exists():
        status_qs.update(is_deleted=True)
        messages.success(request, 'Message removed from inbox.')
        return redirect('messaging:inbox')
    elif msg.sender == request.user:
        msg.delete()
        messages.success(request, 'Message deleted.')
        if 'sent' in referer:
            return redirect('messaging:sent')
        return redirect('messaging:drafts')

    messages.error(request, 'You cannot delete this message.')
    return redirect('messaging:inbox')


@login_required
def unread_count_api(request):
    """JSON endpoint — returns unread count for the navbar badge polling."""
    count = MessageRecipientStatus.objects.filter(
        user=request.user,
        is_read=False,
        is_deleted=False,
        message__status=Message.STATUS_SENT
    ).count()
    return JsonResponse({'unread_count': count})
