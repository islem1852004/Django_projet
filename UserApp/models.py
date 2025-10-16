from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import uuid

def generate_userid():
    return "USER" + uuid.uuid4().hex[:4].upper()

def verify_email(email):
    allowed_domains = ["esprit.tn", "seasame.com", "tek.tn", "central.com"]
    try:
        domain = email.split('@')[1].lower()
        if domain not in allowed_domains:
            raise ValidationError(
                "L'email est invalide et doit appartenir à un domaine universitaire "
                f"({', '.join(allowed_domains)})."
            )
    except IndexError:
        raise ValidationError("L'adresse email est mal formée (format incorrect).")

name_validator = RegexValidator(
    regex=r'^[A-Za-z\s-]+$',
    message="Ce champ doit contenir uniquement des lettres, des espaces ou des tirets."
)

class User(AbstractUser):
    user_id = models.CharField(max_length=8, primary_key=True, unique=True, editable=False)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)  # Nullable username
    first_name = models.CharField(max_length=100, validators=[name_validator])
    last_name = models.CharField(max_length=100, validators=[name_validator])
    email = models.EmailField(unique=True, validators=[verify_email])
    affiliation = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255)
    ROLE = [
        ("participant", "Participant"),
        ("committee", "Membre du comité d'organisation"),
    ]
    role = models.CharField(max_length=255, choices=ROLE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    USERNAME_FIELD = 'email'  # Use email for authentication
    REQUIRED_FIELDS = ['first_name', 'last_name', 'affiliation', 'nationality', 'role']

    def clean(self):
        super().clean()  # Call parent clean method
        verify_email(self.email)  # Validate email

    def save(self, *args, **kwargs):
        self.clean()  # Validate fields before saving
        if not self.user_id:
            new_id = generate_userid()
            while User.objects.filter(user_id=new_id).exists():
                new_id = generate_userid()
            self.user_id = new_id
        super().save(*args, **kwargs)

    class Meta:
        db_table = "users"

class OrganizingCommittee(models.Model):
    user = models.ForeignKey("UserApp.User", on_delete=models.CASCADE, related_name="committee")
    conference = models.ForeignKey("ConferenceAPP.Conference", on_delete=models.CASCADE, related_name="committee")
    ROLES = [
        ("chair", "Président"),
        ("co_chair", "Co-président"),
        ("member", "Membre"),
    ]
    committee_role = models.CharField(max_length=255, choices=ROLES)
    date_joined = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        db_table = "organizing_committee"