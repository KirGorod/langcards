from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
import random

from cards.models import Card, CardProgress, Deck
from .serializers import CardSerializer


class CardViewSet(viewsets.ModelViewSet):
    model = Card
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class LearnCardsView(APIView):
    renderer_classes = [JSONRenderer]
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self._process_get_next_card()

    def post(self, request, *args, **kwargs):
        action = self._validate_aciton(request.data.get('action'))

        if not self._is_valid_action(action):
            return Response(
                data={'error': f'Action {action} is not valid'},
                status=status.HTTP_400_BAD_REQUEST
            )

        progress = get_object_or_404(
            CardProgress,
            card__id=request.data.get('card_id'),
            user=request.user
        )
        progress.handle_action(action)
        return self._process_get_next_card()

    def _is_valid_action(self, action):
        return action in CardProgress.ACTIONS

    def _process_get_next_card(self):
        progress = CardProgress.objects.pop_card(self.request.user)
        if not progress:
            return Response(
                data={'status': 'finished'},
                status=status.HTTP_200_OK
            )

        serializer = CardSerializer(
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


class AddDeckToLearning(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        deck = get_object_or_404(Deck, id=kwargs.get('deck_id'))
        deck.add_to_user(self.request.user)

        return Response(status=status.HTTP_201_CREATED)
