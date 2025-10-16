from django.shortcuts import render
from .models import Conference
from django.views.generic import ListView,DetailView
# Create your views here.
def all_Conferences(req):
    Conferences=Conference.objects.all()
    return render(req,'Conference/liste.html',{"liste":Conferences})
class Conferencelist(ListView):
    model=Conference
    context_object_name="liste"
    ordering=["start_date"]
    template_name="Conference/liste.html"
class ConferenceDetails(DetailView):
    model=Conference
    template_name="Conference/details.html"
    context_object_name="conference"