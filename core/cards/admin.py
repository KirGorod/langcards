from django.contrib import admin

from cards.models import Deck, Card


admin.site.register(Deck)
admin.site.register(Card)
