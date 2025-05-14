from django.db import models
import numpy as np
# Create your models here.

class Image(models.Model):
    path = models.CharField(max_length=255, unique=True)
    image_file = models.FileField(upload_to='images/', null=True, blank=True)  # New field
    description = models.TextField()
    embedding = models.BinaryField()
    similarity = models.FloatField(null=True, blank=True)

    def set_embedding(self, embedding):
        # Convert the numpy array to binary(bytes) for storage
        self.embedding = embedding.tobytes()
    
    def get_embedding(self):
        # Convert the binary data back to a numpy array
        return np.frombuffer(self.embedding, dtype=np.float32)

    def __str__(self):
        return f"Image: {self.path}"

    class Meta:
        db_table = 'images'  # Match the table name from your SQLite schema