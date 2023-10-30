from django.contrib import admin

from cards.models import Deck, Card, CardProgress, CardAdditionalImage


class DeckAdmin(admin.ModelAdmin):
    readonly_fields = ('image_hash',)
    exclude = ('hashed_image',)


class CardAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'word', 'translation', 'deck', 'description', 'image',
    ]
    list_filter = ('deck',)
    search_fields = ('word', 'translation',)
    readonly_fields = ('image_hash',)
    exclude = ('hashed_image',)


class CardAddtionalImageAdmin(admin.ModelAdmin):
    readonly_fields = ('image_hash',)
    exclude = ('hashed_image',)


class CardProgressAdmin(admin.ModelAdmin):
    search_fields = ('user__username'),


admin.site.register(Deck, DeckAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(CardAdditionalImage, CardAddtionalImageAdmin)
admin.site.register(CardProgress, CardProgressAdmin)
