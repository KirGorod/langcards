from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated

from cards.models import Card, CardProgress
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
        progress = CardProgress.objects.pop_card(request.user)

        if not progress:
            return Response(
                data={'status': 'finished'},
                status=status.HTTP_200_OK
            )

        serializer = CardSerializer(progress.card)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        progress = get_object_or_404(
            CardProgress,
            card__id=request.data.get('card_id'),
            user=request.user
        )
        action = self._validate_aciton(request.data.get('action'))

        if not action:
            return Response(
                data={'error': f'Action {action} is not valid'},
                status=status.HTTP_400_BAD_REQUEST
            )

        progress.handle_action(action)
        progress = CardProgress.objects.pop_card(request.user)

        if not progress:
            return Response(
                data={'status': 'finished'},
                status=status.HTTP_200_OK
            )

        serializer = CardSerializer(progress.card)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def _validate_aciton(self, action):
        if action not in ['again', 'hard', 'good']:
            return None
        return action
