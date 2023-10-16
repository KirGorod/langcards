from django.db.models.signals import post_save
from django.dispatch import receiver

from .utils import set_additional_images, generate_hashed_images
from .models import Card, Deck, CardAdditionalImage


@receiver(post_save, sender=Card)
def set_card_images(sender, instance, created, **kwargs):
    if created:
        generate_hashed_images(instance)

    old_instance = sender.objects.get(pk=instance.pk)
    old_image = old_instance.image
    new_image = instance.__dict__.get("image", None)

    if old_image != new_image:
        generate_hashed_images(instance)

    set_additional_images(instance)


@receiver(post_save, sender=Deck)
def set_deck_images(sender, instance, created, **kwargs):
    if created:
        generate_hashed_images(instance)

    old_instance = sender.objects.get(pk=instance.pk)
    old_image = old_instance.image
    new_image = instance.__dict__.get("image", None)

    if old_image != new_image:
        generate_hashed_images(instance)


@receiver(post_save, sender=CardAdditionalImage)
def set_card_additional_images(sender, instance, created, **kwargs):
    if created:
        generate_hashed_images(instance)

    old_instance = sender.objects.get(pk=instance.pk)
    old_image = old_instance.image
    new_image = instance.__dict__.get("image", None)

    if old_image != new_image:
        generate_hashed_images(instance)
