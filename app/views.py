from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import PatientFind
from .models import Patient
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView


class PatientCreate(CreateView):
    model = Patient
    fields = ['last_name', 'first_name', 'dob', 'gender', 'phone', 'phone_2', 'email', 'address', 'consent_hipaa', 'consent_tcpa']


class PatientFind():
    template_name = 'existing-patient.html'
    success_url = '/thanks/'



    def form_valid(self, form) -> HttpResponse:
        # This method is called when valid form data has been POSTed.
        return super().form_valid(form)
