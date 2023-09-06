from django.contrib import admin

from cards.models import Deck, Card, CardProgress, CardAdditionalImage


class CardProgressAdmin(admin.ModelAdmin):
    search_fields = ('user__username'),


admin.site.register(Deck)
admin.site.register(Card)
admin.site.register(CardProgress, CardProgressAdmin)
admin.site.register(CardAdditionalImage)
