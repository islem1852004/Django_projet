# ConferenceAPP/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path("liste/", Conferencelist.as_view(), name="Conferencelist"),
    path("details/<int:pk>/", ConferenceDetails.as_view(), name='Conference_detail'),
    path("form/", ConferenceCreate.as_view(), name="Conference_add"),
    path("<int:pk>/edit/", ConferenceUpdate.as_view(), name="Conference_edit"),
    path("<int:pk>/delete/", ConferenceDetails.as_view(), name="Conference_delete"),
]

