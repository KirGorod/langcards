import random

from rest_framework import serializers

from cards.models import Card
from core.fields import Base64ImageField


class CardSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

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
        count = Card.objects.exclude(
            id=self.instance.id
        ).filter(
            deck=self.instance.deck
        ).count()

        if ans_count >= count:
            raise ValueError(
                'ans_count can\'t be more or equal than overall '
                f'cards count:({count}) in this deck'
            )

        while len(answers) < ans_count:
            random_index = random.randint(0, count - 1)
            answer = Card.objects.exclude(
                id=self.instance.id
            ).filter(
                deck=self.instance.deck
            )[random_index].translation

            if answer not in answers:
                answers.append(answer)

        random.shuffle(answers)
        return answers
