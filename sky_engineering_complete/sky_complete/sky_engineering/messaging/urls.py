from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('inbox/',                      views.inbox,            name='inbox'),
    path('sent/',                       views.sent,             name='sent'),
    path('drafts/',                     views.drafts,           name='drafts'),
    path('compose/',                    views.compose,          name='compose'),
    path('draft/<int:message_id>/',     views.edit_draft,       name='edit_draft'),
    path('view/<int:message_id>/',      views.view_message,     name='view_message'),
    path('toggle/<int:message_id>/',    views.toggle_read,      name='toggle_read'),
    path('delete/<int:message_id>/',    views.delete_message,   name='delete_message'),
    path('api/unread-count/',           views.unread_count_api, name='unread_count_api'),
]
