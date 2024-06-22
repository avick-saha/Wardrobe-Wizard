from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Upper

@receiver(post_delete, sender=Upper)
def delete_upper_file(sender, instance, **kwargs):
    instance.upper.delete(False)
