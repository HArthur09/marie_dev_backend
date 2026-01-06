from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    telephone = models.CharField(max_length=15, null = True, blank = True)

    def __str__(self):
        return self.email