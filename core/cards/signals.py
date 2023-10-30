from django.db.models.signals import post_save
from django.dispatch import receiver

from .utils import set_additional_images
from .tasks import generate_hashed_images
from .models import Card, Deck, CardAdditionalImage


@receiver(post_save, sender=Card, )
def set_card_images(sender, instance, created, **kwargs):
    generate_hashed_images.delay('cards.Card', instance.id)
    set_additional_images(instance)


@receiver(post_save, sender=Deck)
def set_deck_images(sender, instance, created, **kwargs):
    generate_hashed_images.delay('cards.Deck', instance.id)


@receiver(post_save, sender=CardAdditionalImage)
def set_card_additional_images(sender, instance, created, **kwargs):
    generate_hashed_images.delay('cards.CardAdditionalImage', instance.id)
