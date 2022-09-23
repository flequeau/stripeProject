from django import forms

from .models import Patient, Interv


class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ['name', 'forname', 'birthDate', 'phone', 'email']


class IntervForm(forms.ModelForm):

    class Meta:
        model = Interv
        fields = ['patient', 'date', 'amount']