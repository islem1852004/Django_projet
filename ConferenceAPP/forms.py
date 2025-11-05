from django import forms
from .models import Conference
class ConferenceModel(forms.ModelForm):
    class Meta:
        model=Conference
        fields=['name','theme','description','location','start_date','end_date']
        labes={
            'name':"nom de la conference",
            'theme':"thematique",
            'description':"Description",
            'location':"localisation",
            'start_date':"date debut de conference",
            'end_date':"date fin de conference ",
        }
        widgets ={
            'name': forms.TextInput(
                attrs={
                    
                    'placeholder':"EX - conference"
                }
            ),
            'start_date': forms.DateInput(
                attrs={
                    'type':'date',
                    'placeholder':"date de debut"
                }
            ),
            'end_date': forms.DateInput(
                attrs={
                    'type':'date',
                    'placeholder':"date fin"
                }
            )
        }