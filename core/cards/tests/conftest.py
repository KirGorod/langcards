import pytest
from django.db.models.signals import post_save
from cards.models import Card
from cards.signals import set_pixabay_images


@pytest.fixture(autouse=True)
def mute_signals():
    post_save.disconnect(set_pixabay_images, sender=Card)
    yield
    post_save.connect(set_pixabay_images, sender=Card)
