from django.contrib import admin

from cards.models import Deck, Card, CardProgress


admin.site.register(Deck)
admin.site.register(Card)
admin.site.register(CardProgress)
