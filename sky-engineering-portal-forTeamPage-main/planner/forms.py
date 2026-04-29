# Author: Student 4 (Alexandra-Maria Paraschiv)
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'date', 'category']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'title': forms.TextInput(attrs={'placeholder': 'What needs to be done?', 'class': 'form-input'}),
            'description': forms.Textarea(attrs={'rows': 2, 'class': 'form-input'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
        }