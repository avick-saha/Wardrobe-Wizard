from django.db import models
from django.contrib.auth.models import User

class Upper(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upper = models.ImageField(upload_to='uppers/')

    def __str__(self):
        return f"{self.user.username}'s upper"

class Lower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lower = models.ImageField(upload_to='lowers/')

    def __str__(self):
        return f"{self.user.username}'s lower"

class MatchingCombination(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upper = models.ForeignKey(Upper, on_delete=models.CASCADE)
    lower = models.ForeignKey(Lower, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'upper', 'lower')

    def __str__(self):
        return f"Combination for {self.user.username}"
