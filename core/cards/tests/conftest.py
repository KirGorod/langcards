import pytest
from django.db.models.signals import post_save
from cards.models import Card, Deck, CardAdditionalImage
from cards.signals import (set_card_additional_images, set_card_images,
                           set_deck_images)


@pytest.fixture(autouse=True)
def mute_signals():
    post_save.disconnect(
        set_card_additional_images,
        sender=CardAdditionalImage
    )
    post_save.disconnect(set_card_images, sender=Card)
    post_save.disconnect(set_deck_images, sender=Deck)
    yield
    post_save.connect(set_card_additional_images, sender=CardAdditionalImage)
    post_save.connect(set_card_images, sender=Card)
    post_save.connect(set_deck_images, sender=Deck)
