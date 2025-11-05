from django.urls import path
from .views import *
#from . import views
urlpatterns=[
    #path("liste/", views.all_Conferences,name="conference_liste"),
    path("liste/",Conferencelist.as_view(),name="Conferencelist"),
    path("details/<int:pk>/",ConferenceDetails.as_view(),name='Conference_detail'),
    path("form/",ConferenceCreate.as_view(),name="Conference_add"),
    path("<int:pk>/edit/",ConferenceUpdate.as_view(),name="Conference_edit"),
    path("<int:pk>/delete/",ConferencDelete.as_view(),name="Conference_delete")
]
    