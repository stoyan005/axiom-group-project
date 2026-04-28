from messaging.models import MessageRecipientStatus, Message


def unread_count(request):
    """
    Makes unread_count available in all templates globally.
    Used by the base template navbar badge.
    """
    if request.user.is_authenticated:
        count = MessageRecipientStatus.objects.filter(
            user=request.user,
            is_read=False,
            is_deleted=False,
            message__status=Message.STATUS_SENT
        ).count()
        return {'unread_count': count}
    return {'unread_count': 0}
