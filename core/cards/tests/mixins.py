from cards.models import Card, Deck


class ExpectedResponseMixin:
    def _get_test_image_url(self, image):
        return f'http://testserver{image.url}' if image else None

    def _get_expected_card_response(self, card: Card,
                                    additional_images=False) -> dict:
        """
        Get expected response for a given card
        """
        expected_response = {
            'id': card.id,
            'deck': card.deck.id,
            'word': card.word,
            'translation': card.translation,
            'description': card.description,
            'image': self._get_test_image_url(card.image),
            'image_hash': card.image_hash
        }

        if additional_images:
            expected_response.update({
                'additional_images': [
                    {
                        'image': self._get_test_image_url(img.image),
                        'image_hash': img.image_hash
                    }
                    for img in card.additional_images.all()
                ]
            })

        return expected_response

    def _get_expected_deck_response(self, deck: Deck,
                                    cards=False):
        """
        Get expected response for a given deck
        """
        expected_response = {
            'id': deck.id,
            'title': deck.title,
            'default': deck.default,
            'image': self._get_test_image_url(deck.image),
            'image_hash': deck.image_hash
        }

        if cards:
            cards = []
            for card in deck.cards.all():
                cards.append(self._get_expected_card_response(card))
            expected_response.update({'cards': cards})

        return expected_response
