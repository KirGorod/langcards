from cards.models import Card, Deck


class ExpectedResponseMixin:
    def _get_test_image_url(self, image):
        return f'http://testserver{image.url}' if image else None

    def _get_expected_card_response(self, card: Card) -> dict:
        """
        Get expected response for a given card
        """
        return {
            'id': card.id,
            'deck': card.deck.id,
            'word': card.word,
            'translation': card.translation,
            'description': card.description,
            'image': self._get_test_image_url(card.image)
        }

    def _get_expected_deck_response(self, deck: Deck,
                                    cards=False, preview=False):
        """
        Get expected response for a given deck
        """
        expected_response = {
            'id': deck.id,
            'title': deck.title,
            'default': deck.default,
        }

        if preview:
            preview = []
            for card in deck.cards.filter(image__isnull=False)[:3]:
                preview.append(self._get_test_image_url(card.image))
            expected_response.update({'preview': preview})

        if cards:
            cards = []
            for card in deck.cards.all():
                cards.append(self._get_expected_card_response(card))
            expected_response.update({'cards': cards})

        return expected_response
