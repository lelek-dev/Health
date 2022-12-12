from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class HealthUser(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.username