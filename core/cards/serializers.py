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
