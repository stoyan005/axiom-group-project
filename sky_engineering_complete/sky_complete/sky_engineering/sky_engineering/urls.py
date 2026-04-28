"""
Sky Engineering Portal - Main URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # login, logout, password reset
    path('messaging/', include('messaging.urls')),
    # NOTE for teammates: add your app urls here e.g.
    # path('teams/', include('teams.urls')),
    # path('organisation/', include('organisation.urls')),
    # path('schedule/', include('schedule.urls')),
    # path('reports/', include('reports.urls')),
    path('', RedirectView.as_view(url='/messaging/inbox/', permanent=False)),
]
