from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Upper(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upper = models.ImageField(upload_to='uppers/')

    def __str__(self):
        return self.title
    