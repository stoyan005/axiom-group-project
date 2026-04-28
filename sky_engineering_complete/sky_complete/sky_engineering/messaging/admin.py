from django.contrib import admin
from .models import Message, MessageRecipientStatus


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['subject', 'sender', 'status', 'sent_at', 'created_at']
    list_filter = ['status', 'sent_at']
    search_fields = ['subject', 'sender__username', 'body']
    # filter_horizontal = ['recipients']  # Cannot use with through model
    readonly_fields = ['created_at', 'updated_at', 'sent_at']


@admin.register(MessageRecipientStatus)
class MessageRecipientStatusAdmin(admin.ModelAdmin):
    list_display = ['message', 'user', 'is_read', 'read_at', 'is_deleted']
    list_filter = ['is_read', 'is_deleted']
    search_fields = ['user__username', 'message__subject']
