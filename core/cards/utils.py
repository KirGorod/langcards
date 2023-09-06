import requests

from django.conf import settings
from django.core.files.base import ContentFile
from django.utils.text import slugify

from cards.models import CardAdditionalImage


def save_image_from_url(model_instance, field_name, url):
    """
    Download an image from the provided URL and
    save it to the ImageField of the given model instance.

    :param model_instance: Model instance with an ImageField.
    :param field_name: The name of the ImageField in the model.
    :param url: URL of the image to download.
    """

    response = requests.get(url, stream=True)

    if response.status_code == 200 and response.content:
        # Content type e.g. 'image/jpeg'
        content_type = response.headers['content-type']
        # Extracting extension
        extension = content_type.split('/')[-1]

        # Building a filename
        file_name = slugify(url.split('/')[-1]) + '.' + extension

        # Now we'll save the image content to the model's ImageField
        field = getattr(model_instance, field_name)
        field.save(file_name, ContentFile(response.content))
        model_instance.save()


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
