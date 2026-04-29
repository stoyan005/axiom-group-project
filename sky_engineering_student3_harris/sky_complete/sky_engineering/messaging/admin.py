
from django.contrib import admin
from .models import Message, MessageRecipientStatus


class MessageRecipientStatusInline(admin.TabularInline):

    model = MessageRecipientStatus
    extra = 0


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):

    # These columns make it easier to check messages during demonstration/testing.
    list_display = ('subject', 'sender', 'status', 'sent_at', 'created_at')
    list_filter = ('status', 'sent_at', 'created_at')
    search_fields = ('subject', 'body', 'sender__username')
    inlines = [MessageRecipientStatusInline]


@admin.register(MessageRecipientStatus)
class MessageRecipientStatusAdmin(admin.ModelAdmin):

    list_display = ('message', 'user', 'is_read', 'is_deleted', 'read_at')
    list_filter = ('is_read', 'is_deleted', 'read_at')
    search_fields = ('message__subject', 'user__username')
