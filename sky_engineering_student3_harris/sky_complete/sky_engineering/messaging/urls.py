
from django.urls import path
from . import views

# Namespacing means templates can use links like {% url 'messaging:inbox' %}.
app_name = 'messaging'

urlpatterns = [
    # Main message folders.
    path('inbox/', views.inbox, name='inbox'),
    path('sent/', views.sent, name='sent'),
    path('drafts/', views.drafts, name='drafts'),

    # Compose and edit draft workflows.
    path('compose/', views.compose, name='compose'),
    path('draft/<int:message_id>/', views.edit_draft, name='edit_draft'),

    # Single message and message actions.
    path('view/<int:message_id>/', views.view_message, name='view_message'),
    path('toggle/<int:message_id>/', views.toggle_read, name='toggle_read'),
    path('delete/<int:message_id>/', views.delete_message, name='delete_message'),

    # Lightweight JSON endpoint for unread badge behaviour.
    path('api/unread-count/', views.unread_count_api, name='unread_count_api'),
]
