import blurhash

from django.apps import apps

from core.celery import app as celery_app
from cards.utils import set_additional_images
from cards.models import HashedImage


@celery_app.task(name='cards.tasks.generate_hashed_images')
def generate_hashed_images(modelName, instance_id):
    module, model = modelName.split('.')
    instance_model = apps.get_model(module, model)
    try:
        instance = instance_model.objects.get(id=instance_id)
    except instance_model.DoesNotExist:
        return

    if not instance.image:
        return

    try:
        with open(instance.image.path, 'rb') as image_file:
            hash = blurhash.encode(image_file, x_components=4, y_components=3)
            if instance.hashed_image:
                hashed_image = instance.hashed_image
                hashed_image.hash = hash
                hashed_image.save()
            else:
                hashed_image = HashedImage.objects.create(hash=hash)
                instance.hashed_image = hashed_image
                instance.save()
    except FileNotFoundError:
        pass


@celery_app.task(name='cards.tasks.set_additional_images_task')
def set_additional_images_task(card_id):
    set_additional_images(card_id)
