from django.db import models
from django.core.validators import MinLengthValidator, FileExtensionValidator, RegexValidator
from django.core.exceptions import ValidationError
import random
import string
from UserApp.models import User

class Conference(models.Model):
    conference_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(validators=[
        MinLengthValidator(limit_value=30, message="La description doit contenir au minimum 30 caractères")
    ])
    location = models.CharField(max_length=255)
    THEME = [
        ("CS&IA", "Informatique et IA"),
        ("SS", "Sciences sociales"),
        ("SE", "Sciences et ingénierie"),
    ]
    theme = models.CharField(max_length=255, choices=THEME)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("La date de début de la conférence doit être antérieure ou égale à la date de fin")

    class Meta:
        db_table = "conferences"

def validate_keywords(keywords):
    max_keywords = 10
    keyword_list = [kw.strip() for kw in keywords.split(',') if kw.strip()]
    if len(keyword_list) > max_keywords:
        raise ValidationError(f"Le nombre de mots-clés ne doit pas dépasser {max_keywords}.")

def generate_submission_id():
    # Générer une chaîne de 8 caractères hexadécimaux en majuscules
    characters = string.hexdigits.upper()[:16]  # '0123456789ABCDEF'
    random_part = ''.join(random.choices(characters, k=8))
    return f"SUB-{random_part}"

class Submission(models.Model):
    submission_id = models.CharField(
        max_length=12,
        primary_key=True,
        unique=True,
        editable=False,
        validators=[
            RegexValidator(
                regex=r'^SUB-[A-F0-9]{8}$',
                message="L'identifiant doit suivre le format SUB-ABCDEFGH (8 caractères hexadécimaux en majuscules)."
            )
        ]
    )
    user = models.ForeignKey("UserApp.User", on_delete=models.CASCADE, related_name="submissions")
    conference = models.ForeignKey("ConferenceAPP.Conference", on_delete=models.CASCADE, related_name="submissions")
    title = models.TextField()
    abstract = models.TextField()
    keywords = models.TextField(validators=[validate_keywords])
    paper = models.FileField(
        upload_to="papers/",
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        null=True,
        blank=True
    )
    STATUS_CHOICES = [
        ("submitted", "Soumis"),
        ("under_review", "En cours de révision"),
        ("accepted", "Accepté"),
        ("rejected", "Rejeté"),
    ]
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default="submitted")
    paid = models.BooleanField(default=False)
    submission_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.submission_id:
            new_id = generate_submission_id()
            while Submission.objects.filter(submission_id=new_id).exists():
                new_id = generate_submission_id()
            self.submission_id = new_id
        self.clean()
        super().save(*args, **kwargs)

    def clean(self):
        validate_keywords(self.keywords)
        if self.conference and self.submission_date:
            if self.submission_date > self.conference.start_date:
                raise ValidationError(
                    f"La soumission ne peut être faite que pour une conférence à venir "
                    f"(date de début : {self.conference.start_date})."
                )
        if self.user and self.submission_date:
            submissions_same_day = Submission.objects.filter(
                user=self.user,
                submission_date=self.submission_date
            ).exclude(pk=self.submission_id)
            if submissions_same_day.count() >= 3:
                raise ValidationError(
                    "Un participant ne peut soumettre à plus de 3 conférences par jour."
                )

    class Meta:
        db_table = "submissions"