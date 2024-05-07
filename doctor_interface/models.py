from django.db import models

# Create your models here.
from django.db import models

class DoctorSelection(models.Model):
    user_id = models.CharField(max_length=100)
    skin_tone = models.CharField(max_length=100)
    melanoma = models.BooleanField(default=False)
