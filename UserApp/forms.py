# UserApp/forms.py
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User

class UserRegisterFrom(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",        # CORRIGÉ : usermane → username
            "first_name",
            "last_name",
            "email",
            "affiliation",
            "nationality",
            "password1",
            "password2"
        ]
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "nom@esprit.tn"}),
            "password1": forms.PasswordInput(attrs={"placeholder": "Mot de passe"}),
            "password2": forms.PasswordInput(attrs={"placeholder": "Confirmer"}),
        }