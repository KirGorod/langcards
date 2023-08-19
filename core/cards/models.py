from django.db import models


class Deck(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Card(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    word = models.CharField(max_length=255)
    translation = models.CharField(max_length=255)
    image = models.ImageField(upload_to='cards/', blank=True, null=True)

    def __str__(self):
        return f'{self.word} | {self.translation}'
