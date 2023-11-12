import random

from django.utils import timezone
from rest_framework import serializers

from cards.models import Card, CardProgress, Deck, LearningLog
from core.fields import Base64ImageField


class CardSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)

    class Meta:
        model = Card
        fields = [
            'id', 'deck', 'word', 'translation', 'description', 'image',
            'image_hash'
        ]

    def validate_deck(self, deck):
        user = self.context['request'].user

        if deck.user != user:
            raise serializers.ValidationError(
                'This deck cannot be edited by this user.'
            )

        return deck


class CardDetailSerializer(CardSerializer):
    additional_images = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = [
            'id', 'deck', 'word', 'translation', 'description', 'image',
            'additional_images', 'image_hash'
        ]

    def get_additional_images(self, card):
        request = self.context.get('request')
        return [
            {
                'image': request.build_absolute_uri(img.image.url),
                'image_hash': img.image_hash
            }
            for img in card.additional_images.all()
        ]


class LearnCardSerializer(CardDetailSerializer):
    def to_representation(self, instance):
        user = self.context.get('user')
        date = timezone.now().date()
        deck = instance.deck

        words_left = CardProgress.objects.filter(
            card__deck=deck,
            user=user,
            due=date
        ).count()
        words_total = self.context.get('cards_total', 0)

        context = super().to_representation(instance)
        context['answers'] = self._get_random_answers(3)
        context['words_total'] = words_total
        context['words_left'] = words_left

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


class DeckSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)

    class Meta:
        model = Deck
        fields = ['id', 'title', 'default', 'image', 'image_hash']
        extra_kwargs = {
            'default': {'read_only': True},
            'user': {'read_only': True},
        }


class DeckDetailSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many=True, read_only=True)
    image = Base64ImageField(required=False)

    class Meta:
        model = Deck
        fields = ['id', 'title', 'default', 'cards', 'image', 'image_hash']
        extra_kwargs = {
            'default': {'read_only': True},
            'user': {'read_only': True},
            'image': {'read_only': True},
        }
