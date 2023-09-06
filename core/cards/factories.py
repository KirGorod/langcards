import factory

from cards.models import Card, CardAdditionalImage, Deck
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
        skip_postgeneration_save = True

    deck = factory.SubFactory(DeckFactory)
    word = factory.Faker('word')
    translation = factory.Faker('word')
    description = factory.Faker('text')
    image = factory.django.ImageField(color='blue')

    @factory.post_generation
    def add_additional_images(self, create, extracted, **kwargs):
        if not create:
            return

        for _ in range(4):
            CardAdditionalImageFactory(card=self)


class CardAdditionalImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CardAdditionalImage

    card = factory.SubFactory(CardFactory)
    image = factory.django.ImageField(color='red')
