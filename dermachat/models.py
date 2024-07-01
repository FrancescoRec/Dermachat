from django.db import models
import uuid

# Modello per i metadati delle immagini
class ImageMetadata(models.Model):
    """Model to store metadata of images uploaded by users"""
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    skin_tone = models.CharField(max_length=10, default='', blank=True)
    malignant = models.BooleanField(max_length=10, null=True)
    image = models.ImageField(upload_to='raw_data/unlabelled_images/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    prediction = models.FloatField(default=0.0)

    # Definisci la stringa di rappresentazione dell'oggetto
    def __str__(self):
        return str(self.user_id)
    
    # Definisci il nome del file
    @property
    def filename(self):
        filename = f"{self.created_at}_{self.user_id}.jpg"  
        return filename
    
    # Definisci la tabella del database
    class Meta:
        db_table = "dermachat_database"