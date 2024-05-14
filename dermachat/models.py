from django.db import models
import uuid

class ImageMetadata(models.Model):
    """Model to store metadata of images uploaded by users"""
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    skin_tone = models.CharField(max_length=10, default='', blank=True)
    malignant = models.BooleanField(max_length=10, null=True)
    image = models.ImageField(upload_to='raw_data/nonlabelled_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    # Define the string representation of the model
    def __str__(self):
        return str(self.user_id)
    
    # Define the filename property
    @property
    def filename(self):
        filename = f"{self.created_at}_{self.user_id}.jpg"  
        return filename
    
    # Define the name of the database table
    class Meta:
        db_table = "dermachat_database"