from django.db import models
from internalAuth.models import HealthUser
import os
from django.dispatch import receiver


def user_directory_path(instance, filename):
    return 'uploads/user_{0}/record_{1}/{2}'.format(instance.record.folder.owner.pk, instance.record.pk, filename)

# Create your models here.
class HealthRecordFolder(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(default=None, blank=True, null=True)
    owner = models.ForeignKey(HealthUser, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, default=None)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class HealthRecord(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(default=None, blank=True, null=True)
    folder = models.ForeignKey(HealthRecordFolder, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class UserHealthRecordSharing(models.Model):
    title = models.CharField(max_length = 50)
    description = models.TextField(default=None, blank=True, null=True)
    user_id = models.ForeignKey(HealthUser, on_delete=models.CASCADE)
    folder = models.ForeignKey(HealthRecordFolder, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class HealthRecordMedia(models.Model):
    record = models.ForeignKey(HealthRecord, on_delete=models.CASCADE)
    media = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.record.title

@receiver(models.signals.post_delete, sender=HealthRecordMedia)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.media and os.path.isfile(instance.media.path):
        os.remove(instance.media.path)