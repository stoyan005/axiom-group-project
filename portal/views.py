from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .models import Organization, Department, Team

def auth_page(request):
    return render(request, "portal/auth.html")


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('auth')
    else:
        form = UserCreationForm()

    return render(request, 'portal/signup.html', {'form': form})


@login_required
def home(request):
    orgs = Organization.objects.all()
    return render(request, 'portal/home.html', {"orgs": orgs})


@login_required
def organization_list(request):
    orgs = Organization.objects.all()
    return render(request, "portal/organization_list.html", {"orgs": orgs})


@login_required
def organization_detail(request, id):
    org = get_object_or_404(Organization, id=id)
    departments = org.department_set.all()

    return render(request, "portal/organization_detail.html", {
        "org": org,
        "departments": departments
    })


@login_required
def department_detail(request, id):
    department = get_object_or_404(Department, id=id)
    teams = department.team_set.all()

    return render(request, "portal/department_detail.html", {
        "department": department,
        "teams": teams
    })


@login_required
def team_detail(request, id):
    team = get_object_or_404(Team, id=id)

    return render(request, "portal/team_detail.html", {
        "team": team,
        "dependencies": team.dependencies.all()
    })