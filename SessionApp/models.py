from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class Session(models.Model):
    session_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    session_day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_validator = RegexValidator(
        regex=r'^[A-Za-z0-9]+$',
        message="Le nom de la salle doit contenir uniquement des lettres et des chiffres."
    )
    room = models.CharField(max_length=255, validators=[room_validator])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    conference = models.ForeignKey("ConferenceAPP.Conference", on_delete=models.CASCADE, related_name="sessions")
    def clean(self):
        if self.conference and self.session_day:
            if not (self.conference.start_date <= self.session_day <= self.conference.end_date):
                raise ValidationError(
                    f"La date de la session ({self.session_day}) doit être comprise "
                    f"entre la date de début ({self.conference.start_date}) et la "
                    f"date de fin ({self.conference.end_date}) de la conférence."
                )
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError("L'heure de fin doit être postérieure à l'heure de début.")
    class Meta:
        db_table = "sessions"