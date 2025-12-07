# ConferenceAPP/forms.py
from django import forms
from .models import Conference, Submission
from django.utils import timezone

class ConferenceModel(forms.ModelForm):
    class Meta:
        model = Conference
        fields = ['name', 'theme', 'description', 'location', 'start_date', 'end_date']
        labels = {
            'name': "Nom de la conférence",
            'theme': "Thématique",
            'description': "Description",
            'location': "Localisation",
            'start_date': "Date de début",
            'end_date': "Date de fin",
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'EX - IA Summit 2025', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'placeholder': 'Tunis, Tunisie', 'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['conference', 'title', 'abstract', 'keywords', 'paper']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Titre de votre article', 'class': 'form-control'}),
            'abstract': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'keywords': forms.TextInput(attrs={'placeholder': 'IA, ML, NLP', 'class': 'form-control'}),
            'paper': forms.FileInput(attrs={'class': 'form-control'}),
            'conference': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = timezone.now().date()
        self.fields['conference'].queryset = Conference.objects.filter(
            start_date__gte=today
        ).order_by('start_date')