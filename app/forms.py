from django import forms
from django.utils.translation import ugettext_lazy as _


class PatientFindForm(forms.Form):
    # existing_patient = forms.BooleanField()
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    dob = forms.DateField()
    # address = forms.CharField(max_length=255)
    # phone = forms.CharField(max_length=20)
    # consent_hipaa = forms.BooleanField()
    # consent_tcpa = forms.BooleanField()


"""
Are you a new patient?
    Existing:
        First name, last name, date of birth? (or present an employee with your insurance card)
        Has your insurance or phone number changed?
            Yes or I'm not sure: show fields for insurance and phone number info
            No
        Are you using insurance?
    New patient:
        First name, last name, date of birth, address, phone, HIPAA, TCPA
"""
