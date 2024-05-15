from django.db import models
from dermachat.models import ImageMetadata

class DoctorClassification(models.Model):
    """Model to store doctor's classification for images"""
    user_id = models.UUIDField(default=None, null=True, blank=True)
    # image come from the column image in the table ImageMetadata
    image = models.ForeignKey(ImageMetadata, on_delete=models.CASCADE)
    skin_tone = models.IntegerField(choices=[(i, str(i)) for i in range(1, 7)])
    malignant = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "doctor_classification"