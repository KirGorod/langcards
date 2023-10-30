import json
from collections import OrderedDict

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from cards.models import Card, Deck
from cards.factories import CardFactory, DeckFactory
from user.factories import UserFactory
from .mixins import ExpectedResponseMixin


class TestCards(APITestCase, ExpectedResponseMixin):
    def setUp(self) -> None:
        self.deck = DeckFactory.create()
        self.cards = CardFactory.create_batch(5, deck=self.deck)
        self.user = self.deck.user

        self.deck2 = DeckFactory.create()
        self.cards2 = CardFactory.create_batch(3, deck=self.deck2)

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
        Test successful GET single card object
        """
        card = Card.objects.filter(deck__user=self.user).first()
        self.client.force_authenticate(self.user)
        response = self.client.get(
            reverse('cards:cards-detail', kwargs={'pk': card.id})
        )

        expected_data = self._get_expected_card_response(
            card,
            additional_images=True
        )
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

    def test_get_cards_list_success(self):
        """
        Test successful GET list of cards
        """
        self.client.force_authenticate(self.user)
        response = self.client.get(
            reverse('cards:cards-list')
        )

        cards = []
        cards_qs = Card.objects.filter(deck__user=self.user)

        for card in cards_qs:
            card_data = OrderedDict(self._get_expected_card_response(card))
            cards.append(card_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, cards)

    def test_create_card_not_authorized(self):
        """
        Test create card when user is not authenticated
        """
        data = {
            'deck': self.deck.id,
            'word': 'apple',
            'translation': 'яблуко',
            'description': 'some description',
            # 'image': ''
        }
        response = self.client.post(
            reverse('cards:cards-list'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_card_in_not_owned_deck(self):
        """
        Test create card inside not owned deck by this user
        """
        self.client.force_authenticate(self.user)
        data = {
            'deck': self.deck2.id,
            'word': 'apple',
            'translation': 'яблуко',
            'description': 'some description',
            # 'image': ''
        }
        response = self.client.post(
            reverse('cards:cards-list'),
            data=data,
            format='json'
        )

        error_message = json.loads(response.content.decode()).get('deck')[0]
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            error_message,
            'This deck cannot be edited by this user.'
        )

    def test_create_card_success(self):
        """
        Test successful creation of a card
        """
        self.client.force_authenticate(self.user)
        data = {
            'deck': self.deck.id,
            'word': 'apple',
            'translation': 'яблуко',
            'description': 'some description',
            # 'image': ''
        }
        response = self.client.post(
            reverse('cards:cards-list'),
            data=data,
            format='json'
        )
        card = Card.objects.last()
        expected_response = self._get_expected_card_response(card)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response.data, expected_response)

    def test_patch_card_not_authorized(self):
        """
        Test partial update on card when user is not authenticated
        """
        card = self.cards[0]
        data = {
            'word': 'new word',
            'translation': 'new_translation'
        }
        response = self.client.patch(
            reverse('cards:cards-detail', kwargs={'pk': card.id}),
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_not_owned_card(self):
        """
        Test partial update on card that is not owned by user
        """
        self.client.force_authenticate(self.user)
        card = self.cards2[0]
        data = {
            'word': 'new word',
            'translation': 'new_translation'
        }
        response = self.client.patch(
            reverse('cards:cards-detail', kwargs={'pk': card.id}),
            data=data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_card_success(self):
        """
        Test partial update successful
        """
        self.client.force_authenticate(self.user)
        card = self.cards[0]
        data = {
            'word': 'new word',
            'translation': 'new_translation'
        }
        response = self.client.patch(
            reverse('cards:cards-detail', kwargs={'pk': card.id}),
            data=data,
            format='json'
        )
        expected_response = self._get_expected_card_response(
            Card.objects.get(id=card.id)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, expected_response)

    def test_delete_card_not_authenticated(self):
        """
        Test DELETE card without authentication
        """
        card = self.cards[0]
        response = self.client.delete(
            reverse('cards:cards-detail', kwargs={'pk': card.id})
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Card.objects.filter(id=card.id).exists())

    def test_delete_card_not_owned_by_user(self):
        """
        Test DELETE card that is not owned by user
        """
        self.client.force_authenticate(self.user)
        card = self.cards2[0]
        response = self.client.delete(
            reverse('cards:cards-detail', kwargs={'pk': card.id})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Card.objects.filter(id=card.id).exists())

    def test_delete_card_success(self):
        """
        Test successful card deletion
        """
        self.client.force_authenticate(self.user)
        card = self.cards[0]
        response = self.client.delete(
            reverse('cards:cards-detail', kwargs={'pk': card.id})
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Card.objects.filter(id=card.id).exists())


class TestDeck(APITestCase, ExpectedResponseMixin):
    def setUp(self):
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        self.deck = DeckFactory(user=self.user1)
        self.default_deck = DeckFactory(default=True, user=None)
        self.cards = CardFactory.create_batch(5, deck=self.deck)

    def test_get_single_deck_not_authorized(self):
        response = self.client.get(
            reverse('cards:decks-detail', kwargs={'pk': self.deck.id})
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_single_deck_not_owned(self):
        self.client.force_authenticate(self.user2)
        response = self.client.get(
            reverse('cards:decks-detail', kwargs={'pk': self.deck.id})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_default_deck(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(
            reverse('cards:decks-detail', kwargs={'pk': self.default_deck.id})
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_single_deck_not_found(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(
            reverse('cards:decks-detail', kwargs={'pk': 99999})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_single_deck_success(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(
            reverse('cards:decks-detail', kwargs={'pk': self.deck.id})
        )

        expected_response = self._get_expected_deck_response(
            deck=self.deck, cards=True
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_get_decks_list_not_authenticated(self):
        response = self.client.get(
            reverse('cards:decks-list')
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_decks_list_success(self):
        self.client.force_authenticate(self.user1)
        response = self.client.get(
            reverse('cards:decks-list')
        )

        expected_data = []
        expected_data.append(
            self._get_expected_deck_response(self.deck)
        )
        expected_data.append(
            self._get_expected_deck_response(self.default_deck)
        )

        sorted_response_data = sorted(response.data, key=lambda x: x['id'])
        sorted_expected_data = sorted(expected_data, key=lambda x: x['id'])

        sorted_response_data = [dict(item) if isinstance(item, OrderedDict)
                                else item for item in sorted_response_data]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(sorted_response_data, sorted_expected_data)

    def test_add_deck_not_authenticated(self):
        data = {'title': 'New Deck'}
        response = self.client.post(
            reverse('cards:decks-list'),
            data=data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_deck_no_title(self):
        data = {}
        self.client.force_authenticate(self.user1)
        response = self.client.post(
            reverse('cards:decks-list'),
            data=data,
            format='json'
        )
        error_message = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, error_message)

    def test_add_deck_success(self):
        data = {'title': 'New Deck'}
        self.client.force_authenticate(self.user1)
        response = self.client.post(
            reverse('cards:decks-list'),
            data=data,
            format='json'
        )
        deck = Deck.objects.last()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(
            response.data,
            self._get_expected_deck_response(deck)
        )

    def test_update_deck_not_authenticated(self):
        response = self.client.patch(
            reverse('cards:decks-detail', kwargs={'pk': self.deck.id})
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_deck_not_owned(self):
        self.client.force_authenticate(self.user2)
        response = self.client.patch(
            reverse('cards:decks-detail', kwargs={'pk': self.deck.id})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_default_deck(self):
        self.client.force_authenticate(self.user1)
        response = self.client.patch(
            reverse('cards:decks-detail', kwargs={'pk': self.default_deck.id})
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_deck_success(self):
        data = {'title': 'New title'}
        self.client.force_authenticate(self.user1)
        response = self.client.patch(
            reverse('cards:decks-detail', kwargs={'pk': self.deck.id}),
            data=data,
            format='json'
        )
        deck = Deck.objects.get(id=self.deck.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            self._get_expected_deck_response(deck)
        )

    def test_delete_deck_not_authenticated(self):
        response = self.client.delete(
            reverse('cards:decks-detail', kwargs={'pk': self.deck.id})
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_deck_not_owned(self):
        self.client.force_authenticate(self.user2)
        response = self.client.delete(
            reverse('cards:decks-detail', kwargs={'pk': self.deck.id})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_default_deck(self):
        self.client.force_authenticate(self.user1)
        response = self.client.delete(
            reverse('cards:decks-detail', kwargs={'pk': self.default_deck.id})
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_deck_success(self):
        self.client.force_authenticate(self.user1)
        response = self.client.delete(
            reverse('cards:decks-detail', kwargs={'pk': self.deck.id})
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
