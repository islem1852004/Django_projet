# ConferenceAPP/views.py
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Conference
from .forms import ConferenceModel


class Conferencelist(LoginRequiredMixin, ListView):
    model = Conference
    context_object_name = "liste"
    ordering = ["start_date"]
    template_name = "Conference/liste.html"


class ConferenceDetails(DetailView):
    model = Conference
    template_name = "Conference/details.html"
    context_object_name = "conference"


class ConferenceCreate(LoginRequiredMixin, CreateView):
    model = Conference
    form_class = ConferenceModel
    template_name = "Conference/conference_form.html"
    success_url = reverse_lazy("Conferencelist")

    def form_valid(self, form):
        messages.success(self.request, "Conférence ajoutée avec succès.")
        return super().form_valid(form)


class ConferenceUpdate(LoginRequiredMixin, UpdateView):
    model = Conference
    form_class = ConferenceModel
    template_name = "Conference/conference_form.html"
    success_url = reverse_lazy("Conferencelist")

    def get_queryset(self):
        # Plus de filtrage sur committee → on autorise tous les admins ou superusers
        # Ou tu peux ajouter une logique plus tard
        return Conference.objects.all()

    def form_valid(self, form):
        messages.success(self.request, "Conférence modifiée avec succès.")
        return super().form_valid(form)


class ConferencDelete(LoginRequiredMixin, DeleteView):
    model = Conference
    template_name = "Conference/conference_confirm_delete.html"
    success_url = reverse_lazy("Conferencelist")

    def get_queryset(self):
        return Conference.objects.all()

    def form_valid(self, form):
        messages.success(self.request, "Conférence supprimée avec succès.")
        return super().form_valid(form)