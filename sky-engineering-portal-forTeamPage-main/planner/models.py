# Author: Student 4 (Alexandra-Maria Paraschiv)
# Contribution: Backend Database Model for Calendar Tasks

from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    
    CATEGORY_CHOICES = [
        ('maths', 'Maths'),
        ('project', 'Project'),
        ('personal', 'Personal'),
    ]
    
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='personal')

    def __str__(self):
        return self.title