from django.apps import AppConfig


class CardsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cards'

    def ready(self):
        from .signals import set_pixabay_images
