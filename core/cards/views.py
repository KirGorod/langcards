from rest_framework import viewsets

from cards.models import Card
from .serializers import CardSerializer


class CardViewSet(viewsets.ModelViewSet):
    model = Card
    queryset = Card.objects.all()
    serializer_class = CardSerializer
