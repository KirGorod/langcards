import requests

from django.core.files.base import ContentFile
from django.utils.text import slugify


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
