from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('auth/', views.auth_page, name='auth'),

    path('login/', auth_views.LoginView.as_view(
        template_name='portal/auth.html'
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('signup/', views.signup, name='signup'),

    path('organizations/', views.organization_list, name='organization_list'),
    path('organizations/<int:id>/', views.organization_detail, name='organization_detail'),

    path('departments/<int:id>/', views.department_detail, name='department_detail'),
    path('teams/<int:id>/', views.team_detail, name='team_detail'),
]