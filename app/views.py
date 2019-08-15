from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic.edit import FormView
from .forms import PatientFindForm
from .models import Patient
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView


class PatientCreate(CreateView):
    model = Patient
    fields = ['last_name', 'first_name', 'dob', 'gender', 'phone', 'phone_2', 'email', 'address', 'consent_hipaa', 'consent_tcpa']


class PatientFindView(FormView):
    template_name = 'existing-patient.html'
    form_class = PatientFindForm
    success_url = '/thanks/'

    def form_valid(self, form) -> HttpResponse:
        # This method is called when valid form data has been POSTed.
        return super().form_valid(form)
