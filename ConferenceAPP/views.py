from django.shortcuts import render
from .models import Conference
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from .forms import ConferenceModel
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
class ConferenceCreate(CreateView):
    model=Conference
    template_name="Conference/Conference_form.html"
    #fields="__all__"
    form_class =ConferenceModel
    success_url=reverse_lazy("Conferencelist")
class ConferenceUpdate(UpdateView):
    model=Conference
    template_name="Conference/Conference_form.html"
    #fields="__all__"
    form_class =ConferenceModel
    success_url=reverse_lazy("Conferencelist")
class ConferencDelete(DeleteView):
    model=Conference
    template_name="Conference/Conference_confirm_delete.html"
    success_url=reverse_lazy("Conferencelist")