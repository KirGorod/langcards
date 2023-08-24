import random

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from cards.models import Card
from .serializers import CardSerializer


class CardViewSet(viewsets.ModelViewSet):
    model = Card
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class RandomCardView(APIView):
    def get(self, request, *args, **kwargs):
        cards = Card.objects.all()
        if not cards:
            return Response(status=status.HTTP_404_NOT_FOUND)

        random_card = random.choice(cards)
        serializer = CardSerializer(instance=random_card)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
