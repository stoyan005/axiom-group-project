from django.urls import path
from . import teams

urlpatterns = [
    path('', teams.index)
]