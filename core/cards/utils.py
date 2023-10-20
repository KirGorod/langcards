import blurhash
import requests

from django.conf import settings

from cards.models import CardAdditionalImage
from core.utils import save_image_from_url


def set_additional_images(card):
    if card.additional_images.count() == 4:
        return

    key = settings.PIXABAY_API_KEY
    query = card.word.replace(' ', '+')
    url = (
        f'https://pixabay.com/api/?'
        f'key={key}&q={query}&image_type=photo&per_page=4'
    )
    response = requests.get(url)
    CardAdditionalImage.objects.filter(card=card).delete()

    if response.status_code == 200:
        data = response.json()
        for item in data.get('hits'):
            card_image = CardAdditionalImage.objects.create(card=card)
            save_image_from_url(card_image, 'image', item.get('largeImageURL'))


def generate_hashed_images(instance):
    if not instance.image:
        return

    try:
        with open(instance.image.path, 'rb') as image_file:
            hash = blurhash.encode(image_file, x_components=4, y_components=3)
            instance.image_hash = hash
            instance.save()
    except FileNotFoundError:
        pass
