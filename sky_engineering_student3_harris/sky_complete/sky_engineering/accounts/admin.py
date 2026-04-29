
from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    # Columns shown on the admin list page.
    list_display = ('user', 'job_title', 'department', 'slack_handle', 'updated_at')

    # Search helps admins find a profile by user or department details.
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'department')

    # Filters are useful when there are many users across multiple departments.
    list_filter = ('department', 'created_at')
