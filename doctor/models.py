from django.db import models
from internalAuth.models import HealthUser
from healthRecords.models import HealthRecord

# Create your models here.
class Patients(models.Model):
    doctor = models.ForeignKey(HealthUser, null=True, related_name="doctor", on_delete=models.CASCADE)
    user = models.ForeignKey(HealthUser, null=True, related_name="user", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.doctor.username

class ShareRecordDoctor(models.Model):
    patient = models.ForeignKey(Patients, null=True, related_name="patient", on_delete=models.CASCADE)
    record = models.ForeignKey(HealthRecord, null=True, related_name="record", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.record

class InvitesDoctor(models.Model):
    doctor = models.ForeignKey(HealthUser, null=True, related_name="invite_doctor", on_delete=models.CASCADE)
    user = models.ForeignKey(HealthUser, null=True, related_name="invite_user", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.doctor.username