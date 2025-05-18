from django.db import models
import pickle
# Create your models here.

class Image(models.Model):
    path = models.CharField(max_length=255)
    image_file = models.FileField(upload_to='images/', null=True, blank=True)  # New field
    description = models.TextField(blank=True)
    embedding = models.BinaryField(blank=True) 
    similarity = models.FloatField(null=True, blank=True)

    def set_embedding(self, embedding):
        # Convert the numpy array to binary(bytes) for storage
        self.embedding = pickle.dumps(embedding)
    
    def get_embedding(self):
        # Convert the binary data back to a numpy array
        return pickle.loads(self.embedding)

    def __str__(self):
        return f"Image: {self.path}"

    class Meta:
        db_table = 'images'  # Match the table name from your SQLite schema