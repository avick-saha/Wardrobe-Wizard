from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='cloths/')
    uploaded_at = models.DateTimeField(auto_now_add=True)