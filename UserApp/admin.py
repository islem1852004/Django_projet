# UserApp/admin.py
from django.contrib import admin
from .models import User, OrganizingCommittee

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'email', 'first_name', 'last_name', 'role', 'affiliation', 'nationality']
    search_fields = ['user_id', 'email', 'first_name', 'last_name']
    list_filter = ['role', 'created_at']
    ordering = ['email']
    readonly_fields = ['user_id', 'created_at', 'updated_at']

@admin.register(OrganizingCommittee)
class OrganizingCommitteeAdmin(admin.ModelAdmin):
    list_display = ['user', 'conference', 'committee_role', 'date_joined']
    search_fields = ['user__email', 'conference__name']
    list_filter = ['committee_role', 'date_joined']
    ordering = ['date_joined']
    readonly_fields = ['created_at', 'updated_at']