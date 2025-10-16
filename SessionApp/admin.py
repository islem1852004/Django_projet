# SessionApp/admin.py
from django.contrib import admin
from .models import Session

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'title', 'topic', 'session_day', 'start_time', 'end_time', 'room', 'conference']
    search_fields = ['title', 'topic', 'room', 'conference__name']
    list_filter = ['session_day', 'conference']
    ordering = ['session_day', 'start_time']
    readonly_fields = ['session_id', 'created_at', 'updated_at']