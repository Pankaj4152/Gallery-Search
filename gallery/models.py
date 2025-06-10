from django.db import models
from django.contrib.auth.models import User
import numpy as np
import pickle

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/images/user_<id>/<filename>
    return f'images/user_{instance.user.id}/{filename}'

class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images')
    path = models.CharField(max_length=255, null=True)
    image_file = models.FileField(upload_to='images/', null=True, blank=True) 
    description = models.TextField(blank=True)
    embedding = models.BinaryField(blank=True) 

    def set_embedding(self, embedding):
        # Convert the numpy array to binary for storage
        self.embedding = pickle.dumps(embedding)
    
    def get_embedding(self):
        # Convert the binary data back to array
        return pickle.loads(self.embedding)

    def __str__(self):
        return f"Image: {self.path}"

    class Meta:
        db_table = 'images'