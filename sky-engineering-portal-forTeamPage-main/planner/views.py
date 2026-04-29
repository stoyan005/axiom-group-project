# Author: Student 4
# Contribution: Logic to generate calendar grid and fetch user tasks

import calendar
from datetime import datetime
from django.shortcuts import render
from .models import Task

def calendar_view(request):
    today = datetime.now()
    curr_year = today.year
    curr_month = today.month

    tasks = Task.objects.filter(date__year=curr_year, date__month=curr_month)

    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(curr_year, curr_month)

    context = {
        'month_days': month_days,
        'tasks': tasks,
        'curr_month_name': today.strftime('%B'),
        'curr_year': curr_year,
    }
    
    return render(request, 'planner/calendar.html', context)