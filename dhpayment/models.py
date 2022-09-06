import uuid as uuid
from django.db import models
from django.urls import reverse


class Patient(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Nom")
    forname = models.CharField(max_length=50, blank=True, null=True, verbose_name="Prénom")
    phone = models.CharField(max_length=10, blank=True, null=True, verbose_name="Téléphone")
    email = models.EmailField(blank=True, null=True)
    birthDate = models.DateField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('patient_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '{} {}'.format(self.forname, self.name)

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
        ordering = ['name']


class Interv(models.Model):
    patient = models.ForeignKey(Patient, blank=True, null=True, verbose_name="Patient", on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True, verbose_name="Date Interv.")
    amount = models.IntegerField(blank=True, null=True, verbose_name="Montant DH")
    uuid = models.CharField(max_length=50, blank=True, null=True, verbose_name="Identifiant paiement")

    def get_absolute_url(self):
        return reverse('interv_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '{} {}'.format(self.patient, self.date)

    class Meta:
        verbose_name = 'Intervention'
        verbose_name_plural = 'Interventions'
        ordering = ['date']
