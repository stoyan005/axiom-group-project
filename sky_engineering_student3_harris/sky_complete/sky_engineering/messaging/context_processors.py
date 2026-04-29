
from .models import MessageRecipientStatus, Message


def unread_count(request):

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
