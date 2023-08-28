import factory

from cards.models import Card, Deck
from user.factories import UserFactory


class DeckFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Deck

    title = factory.Sequence(lambda n: f'Deck {n}')
    default = False
    user = factory.SubFactory(UserFactory)


class CardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Card

    deck = factory.SubFactory(DeckFactory)
    word = factory.Faker('word')
    translation = factory.Faker('word')
    description = factory.Faker('text')
    image = factory.django.ImageField(color='blue')
