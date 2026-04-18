from django.urls import path
from . import organisation

#Define a list of url patterns
urlpatterns = [
    path('', organisation.index)
]