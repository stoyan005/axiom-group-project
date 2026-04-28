"""
Main URL configuration for the Sky Engineering Portal.

This file connects the project-level routes to the individual Django apps.  It is
also the integration point where other group members can include their own app
URLs without changing the messaging code.
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # Django admin provides the administrator interface required by the brief.
    path('admin/', admin.site.urls),

    # Custom account pages such as registration, profile and change password.
    path('accounts/', include('accounts.urls')),

    # Built-in Django auth URLs provide login and logout routes.
    path('accounts/', include('django.contrib.auth.urls')),

    # Student 3 messaging pages: inbox, sent, drafts, compose and message view.
    path('messaging/', include('messaging.urls')),

    # Future group apps can be connected using the same pattern, for example:
    # path('teams/', include('teams.urls')),
    # path('organisation/', include('organisation.urls')),
    # path('schedule/', include('schedule.urls')),
    # path('reports/', include('reports.urls')),

    # The home URL redirects users to the main application area.
    path('', RedirectView.as_view(url='/messaging/inbox/', permanent=False)),
]
