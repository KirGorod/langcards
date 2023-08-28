from collections import OrderedDict

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from cards.models import Card
from cards.factories import CardFactory, DeckFactory
from core.utils import get_test_image_url


class TestCards(APITestCase):
    def setUp(self) -> None:
        self.deck = DeckFactory.create()
        self.cards = CardFactory.create_batch(5, deck=self.deck)
        self.user = self.deck.user

        deck2 = DeckFactory.create()
        CardFactory.create_batch(3, deck=deck2)

    def test_get_single_card_not_authorized(self):
        """
        Test GET single card when user is not authorized
        """
        card = Card.objects.filter(deck__user=self.user).first()
        response = self.client.get(
            reverse('cards:cards-detail', kwargs={'pk': card.id})
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_single_card_success(self):
        """
        Test successfull GET single card object
        """
        card = Card.objects.filter(deck__user=self.user).first()
        self.client.force_authenticate(self.user)
        response = self.client.get(
            reverse('cards:cards-detail', kwargs={'pk': card.id})
        )

        expected_data = self._get_expected_response(card)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, expected_data)

    def test_get_cards_list_not_authorized(self):
        """
        Test GET list of cards when user is not authorized
        """
        response = self.client.get(
            reverse('cards:cards-list')
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_carsd_list_success(self):
        """
        Test successfull GET list of cards
        """
        self.client.force_authenticate(self.user)
        response = self.client.get(
            reverse('cards:cards-list')
        )

        cards = []
        cards_qs = Card.objects.filter(deck__user=self.user)

        for card in cards_qs:
            card_data = OrderedDict(self._get_expected_response(card))
            cards.append(card_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, cards)

    def _get_expected_response(self, card: Card) -> dict:
        """
        Get expected response for a given card
        """
        return {
            'id': card.id,
            'deck': card.deck.id,
            'word': card.word,
            'translation': card.translation,
            'description': card.description,
            'image': get_test_image_url(card.image)
        }
