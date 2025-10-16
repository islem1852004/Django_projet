# ConferenceAPP/admin.py
from django.contrib import admin
from .models import Conference, Submission

# Inline pour les soumissions (Stacked)
class SubmissionStackedInline(admin.StackedInline):
    model = Submission
    extra = 1
    fields = ['submission_id', 'title', 'abstract', 'status', 'paid', 'user', 'submission_date']
    readonly_fields = ['submission_id', 'submission_date']
    can_delete = True

# Inline pour les soumissions (Tabular)
class SubmissionTabularInline(admin.TabularInline):
    model = Submission
    extra = 1
    fields = ['title', 'status', 'user', 'paid']
    readonly_fields = ['submission_id', 'submission_date']
    can_delete = True

@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    # Affichage dans la liste (déjà inclus dans la demande précédente)
    list_display = ['name', 'theme', 'location', 'start_date', 'end_date', 'duration']
    # Filtres
    list_filter = ['theme', 'location', 'start_date']
    # Recherche
    search_fields = ['name', 'description', 'location']
    # Améliorations visuelles
    ordering = ['start_date']
    date_hierarchy = 'start_date'
    # Champs en lecture seule
    readonly_fields = ['conference_id', 'created_at', 'updated_at']
    # Organisation des champs dans le formulaire
    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'theme', 'description')
        }),
        ('Logistique', {
            'fields': ('location', 'start_date', 'end_date')
        }),
        ('Métadonnées', {
            'fields': ('conference_id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    # Inline pour les soumissions
    inlines = [SubmissionStackedInline]  # Remplacez par SubmissionTabularInline pour tester la version tabulaire
    # Méthode personnalisée pour la durée
    def duration(self, obj):
        duration_days = (obj.end_date - obj.start_date).days
        return duration_days if duration_days >= 0 else "Dates invalides"
    duration.short_description = 'Durée (jours)'

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    # Affichage dans la liste
    list_display = ['title', 'status', 'user', 'conference', 'submission_date', 'paid', 'short_abstract']
    # Champs modifiables directement
    list_editable = ['status', 'paid']
    # Filtres
    list_filter = ['status', 'paid', 'conference', 'submission_date']
    # Recherche
    search_fields = ['title', 'keywords', 'user__username']
    # Champs en lecture seule
    readonly_fields = ['submission_id', 'submission_date', 'created_at', 'updated_at']
    # Organisation des champs dans le formulaire
    fieldsets = (
        ('Infos générales', {
            'fields': ('submission_id', 'title', 'abstract', 'keywords')
        }),
        ('Fichier et conférence', {
            'fields': ('paper', 'conference')
        }),
        ('Suivi', {
            'fields': ('status', 'paid', 'submission_date', 'user')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    # Actions personnalisées
    def mark_as_paid(self, request, queryset):
        queryset.update(paid=True)
    mark_as_paid.short_description = "Marquer les soumissions comme payées"

    def accept_submissions(self, request, queryset):
        queryset.update(status='accepted')
    accept_submissions.short_description = "Accepter les soumissions"

    actions = ['mark_as_paid', 'accept_submissions']
    # Méthode personnalisée pour l'abstract tronqué
    def short_abstract(self, obj):
        return obj.abstract[:50] + ('...' if len(obj.abstract) > 50 else '')
    short_abstract.short_description = 'Résumé (50 caractères)'