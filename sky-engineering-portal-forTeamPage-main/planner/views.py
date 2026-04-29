# Author: Student 4 (Alexandra-Maria Paraschiv)
# Contribution: Logic to generate calendar grid and fetch user tasks

from django.shortcuts import render, redirect
from .forms import TaskForm
from .models import Task
from datetime import datetime
import calendar

def calendar_view(request):
    today = datetime.now()
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('calendar_home')
    else:
        form = TaskForm()

    tasks = Task.objects.filter(user=request.user, date__month=today.month)
    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(today.year, today.month)

    return render(request, 'planner/calendar.html', {
        'month_days': month_days,
        'tasks': tasks,
        'form': form,
        'curr_month_name': today.strftime('%B'),
        'curr_year': today.year,
    })