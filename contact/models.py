from django.db import models

# Create your models here.
class ContactUs(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(db_index=True, unique=True, max_length=255)
    message = models.TextField()
    
    def __str__(self):
        return self.full_name
