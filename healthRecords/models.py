from django.db import models
from internalAuth.models import HealthUser

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/record_{1}/{2}'.format(instance.user.id, instance.id ,filename)

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
    media = models.FileField(upload_to='uploads/', null=True, blank=True)
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