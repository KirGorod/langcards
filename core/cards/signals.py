from django.db.models.signals import post_save
from django.dispatch import receiver

from .utils import set_additional_images
from .models import Card


@receiver(post_save, sender=Card)
def set_pixabay_images(sender, instance, created, **kwargs):
    set_additional_images(instance)
