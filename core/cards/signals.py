from django.db.models.signals import post_save
from django.db import transaction
from django.dispatch import receiver
from django.conf import settings

from .tasks import generate_hashed_images, set_additional_images_task
from .models import Card, Deck, CardAdditionalImage


def generate_hash(created, model_name, instance):
    if created:
        transaction.on_commit(
            lambda: generate_hashed_images.delay(model_name, instance.pk)
        )
    else:
        generate_hashed_images.delay(model_name, instance.id)


@receiver(post_save, sender=Card)
def set_card_images(sender, instance, created, **kwargs):
    api_key = settings.PIXABAY_API_KEY
    generate_hash(created, 'cards.Card', instance)

    if created:
        set_additional_images_task.delay(instance.id, api_key)
    else:
        set_additional_images_task.delay(instance.id, api_key)


@receiver(post_save, sender=Deck)
def set_deck_images(sender, instance, created, **kwargs):
    generate_hash(created, 'cards.Deck', instance)


@receiver(post_save, sender=CardAdditionalImage)
def set_card_additional_images(sender, instance, created, **kwargs):
    generate_hash(created, 'cards.CardAdditionalImage', instance)
