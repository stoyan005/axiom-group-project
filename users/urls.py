from django.urls import path
from . import users

#Define a list of url patterns
urlpatterns = [
    path('', users.index)
]