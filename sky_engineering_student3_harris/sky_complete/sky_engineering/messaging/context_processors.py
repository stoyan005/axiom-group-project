"""
Context processors for the messaging app.

A context processor adds values to every template automatically.  Here it allows
the navbar to show the unread message count without every view repeating the same
query.
"""

from .models import MessageRecipientStatus, Message


def unread_count(request):
    """Return the unread message count for authenticated users."""

    if request.user.is_authenticated:
        count = MessageRecipientStatus.objects.filter(
            user=request.user,
            is_read=False,
            is_deleted=False,
            message__status=Message.STATUS_SENT
        ).count()
        return {'unread_count': count}

    # Anonymous users do not have an inbox, so the count is zero.
    return {'unread_count': 0}
