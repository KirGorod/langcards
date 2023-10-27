import blurhash

from django.apps import apps
from django.db.models.signals import post_save

from core.celery import app as celery_app
from cards.models import Card


@celery_app.task(name='cards.tasks.generate_hashed_images')
def generate_hashed_images(modelName, instance_id):
    from cards.signals import set_card_images
    post_save.disconnect(set_card_images, sender=Card)

    module, model = modelName.split('.')
    instance_model = apps.get_model(module, model)
    instance = instance_model.objects.get(id=instance_id)

    if not instance.image:
        return

    try:
        with open(instance.image.path, 'rb') as image_file:
            hash = blurhash.encode(image_file, x_components=4, y_components=3)
            instance.image_hash = hash
            instance.save()
    except FileNotFoundError:
        pass

    post_save.connect(set_card_images, sender=Card)
