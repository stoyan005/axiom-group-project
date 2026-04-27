from django.contrib import admin
from .models import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')

    search_fields = ('name', 'description')

    list_filter = ('name',)

    ordering = ('name',)

    list_per_page = 10

    list_display_links = ('id', 'name')

    list_editable = ('description',)

    fieldsets = (
        ('Team Information', {
            'fields': ('name', 'description')
        }),
    )

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = 'Team Management Dashboard'
        return super().changelist_view(request, extra_context=extra_context)