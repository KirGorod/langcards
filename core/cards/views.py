import random

from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from cards.models import Card, CardProgress, Deck
from .serializers import (
    CardSerializer,
    DeckSerializer,
    LearnCardSerializer,
    DeckDetailSerializer
)


class CardViewSet(viewsets.ModelViewSet):
    renderer_classes = [JSONRenderer]
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]

    model = Card
    serializer_class = CardSerializer

    def get_object(self):
        card = super().get_object()
        user = self.request.user

        if user != card.deck.user:
            raise PermissionDenied("You are not allowed to edit this card.")
        return card

    def get_queryset(self):
        user = self.request.user
        return Card.objects.filter(deck__user=user)


class DeckViewSet(viewsets.ModelViewSet):
    renderer_classes = [JSONRenderer]
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]
    model = Deck
    serializer_class = DeckSerializer

    def get_object(self):
        deck = super().get_object()
        user = self.request.user
        if user != deck.user or deck.default:
            raise PermissionDenied("You are not allowed to edit this deck.")
        return deck

    def get_queryset(self):
        user = self.request.user
        return Deck.objects.filter(
            Q(default=True) | Q(user=user)
        )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DeckDetailSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LearnCardsView(APIView):
    renderer_classes = [JSONRenderer]
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        deck = get_object_or_404(Deck, id=kwargs.get('deck_id'))
        return self._process_get_next_card(deck)

    def post(self, request, *args, **kwargs):
        deck = get_object_or_404(Deck, id=kwargs.get('deck_id'))
        action = self._validate_aciton(request.data.get('action'))

        if not self._is_valid_action(action):
            return Response(
                data={'error': f'Action {action} is not valid'},
                status=status.HTTP_400_BAD_REQUEST
            )

        progress = get_object_or_404(
            CardProgress,
            card__id=request.data.get('card_id'),
            card__deck=deck,
            user=request.user
        )
        progress.handle_action(action)
        return self._process_get_next_card(deck)

    def _is_valid_action(self, action):
        return action in CardProgress.ACTIONS

    def _process_get_next_card(self, deck):
        progress = CardProgress.objects.pop_card(self.request.user, deck)
        if not progress:
            return Response(
                data={'status': 'finished'},
                status=status.HTTP_200_OK
            )

        serializer = LearnCardSerializer(
            progress.card,
            context={'request': self.request}
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def _validate_aciton(self, action):
        if action not in ['again', 'hard', 'good']:
            return None
        return action


class RandomCardView(APIView):
    def get(self, request, *args, **kwargs):
        cards = Card.objects.all()
        if not cards:
            return Response(status=status.HTTP_404_NOT_FOUND)

        random_card = random.choice(cards)
        serializer = CardSerializer(
            instance=random_card,
            context={'request': request}
        )
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )


class AddDeckToLearningView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        deck = get_object_or_404(Deck, id=kwargs.get('deck_id'))
        deck.add_to_user(self.request.user)

        return Response(status=status.HTTP_201_CREATED)
