from django.apps import AppConfig

# clown

class CardsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cards'

    def ready(self):
        from .signals import set_card_images,\
            set_deck_images, set_card_additional_images
