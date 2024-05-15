from django.db import models
from dermachat.models import ImageMetadata

class DoctorClassification(models.Model):
    """Model to store doctor's classification for images"""
    user_id = models.UUIDField(default=None, null=True, blank=True)
    image = models.ImageField(upload_to ='prepared/classified_images/images_of_users', blank=True)
    skin_tone = models.IntegerField(choices=[(i, str(i)) for i in range(1, 7)])
    malignant = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "doctor_classification"