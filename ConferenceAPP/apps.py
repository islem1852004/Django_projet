from django.apps import AppConfig

class ConferenceAppConfig(AppConfig):  # Corrigé : "ConferanceappConfig" → "ConferenceAppConfig"
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ConferenceAPP'  # Correct, correspond au nom du dossier