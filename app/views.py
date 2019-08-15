from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic.edit import FormView
from .forms import PatientFindForm
from .models import Patient
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView


class PatientCreate(CreateView):
    model = Patient
    fields = ['last_name', 'first_name', 'dob', 'gender', 'phone', 'phone_2', 'email', 'address', 'consent_hipaa', 'consent_tcpa', 'diabetes', 'hypertension', 'hypercholesterolemia']

    def get_success_url(self):
        return self.object.get_admin_url()
