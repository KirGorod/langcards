import random

from rest_framework import serializers

from cards.models import Card, Deck
from core.fields import Base64ImageField


class DeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deck
        fields = ['id', 'title', 'default',]
        extra_kwargs = {
            'default': {'read_only': True},
            'user': {'read_only': True},
        }


class CardSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)

    class Meta:
        model = Card
        fields = [
            'id', 'deck', 'word', 'translation', 'image'
        ]


class LearnCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = [
            'id', 'deck', 'word', 'translation', 'image'
        ]

    def to_representation(self, instance):
        context = super().to_representation(instance)
        context['answers'] = self._get_random_answers(3)

        return context

    def _get_random_answers(self, ans_count: int) -> list:
        """
        Get answers for a quiz with ans_count wrong answers
        """
        answers = [self.instance.translation]
        count = Card.objects.filter(
            deck=self.instance.deck
        ).count()

        if ans_count >= count:
            cards = Card.objects.filter(deck=self.instance.deck)
            answers = [card.translation for card in cards]
        else:
            while len(answers) < ans_count:
                random_index = random.randint(0, count - 1)
                answer = Card.objects.filter(
                    deck=self.instance.deck
                )[random_index].translation

                if answer not in answers:
                    answers.append(answer)

        random.shuffle(answers)
        return answers
