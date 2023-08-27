from datetime import timedelta
from django.db import models
from django.utils import timezone


class Deck(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    def add_to_user(self, user):
        """
        Add all cards from the Deck to user's learning progress
        """
        for card in self.cards.all():
            CardProgress.objects.get_or_create(
                user=user,
                card=card
            )


class Card(models.Model):
    deck = models.ForeignKey(
        Deck,
        on_delete=models.CASCADE,
        related_name='cards'
    )
    word = models.CharField(max_length=255)
    translation = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='cards/', blank=True, null=True)

    def __str__(self):
        return f'{self.word} | {self.translation}'


class CardProgressManager(models.Manager):
    def pop_card(self, user, deck):
        """
        Get first card to learn
        """
        return self.filter(
            user=user,
            card__deck=deck,
            due=timezone.now()
        ).order_by('priority').first()


class CardProgress(models.Model):
    NEW = 0
    LEARNING = 1
    REVIEW = 2
    RELEARNING = 3
    CARD_STAGES = (
        (NEW, 'New'),
        (LEARNING, 'Learning'),
        (REVIEW, 'Review'),
        (RELEARNING, 'Relearning')
    )

    ACTIONS = ['again', 'hard', 'good']

    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='card_progress'
    )
    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name='card_progress'
    )
    stage = models.PositiveSmallIntegerField(choices=CARD_STAGES, default=NEW)
    due = models.DateField(default=timezone.now)
    interval = models.IntegerField(default=10)
    ease = models.DecimalField(max_digits=5, decimal_places=2, default=1.85)
    priority = models.PositiveSmallIntegerField(default=1)
    objects = CardProgressManager()

    def __str__(self):
        return f'{self.user.username}`s progress for card {self.card.word}'

    def again(self):
        interval = self.interval * 1.25
        if self.stage in [self.NEW, self.LEARNING]:
            interval = 1
        self._update_progress(interval, priority=2)

    def hard(self):
        interval = self.interval * 1.35
        if self.stage in [self.NEW, self.LEARNING]:
            interval = 2
        self._update_progress(interval, priority=3)

    def good(self):
        interval = self.interval * self.ease
        if self.stage in [self.NEW, self.LEARNING]:
            interval = 3
        self._update_progress(interval)

    def _update_progress(self, new_interval, priority=None, new_ease=None):
        if self.stage == self.NEW:
            self.stage = self.LEARNING

        if new_ease:
            self.ease = new_ease

        if priority:
            self.priority = priority
        else:
            self.priority = 1
            self.due = timezone.now() + timedelta(days=new_interval)

        self.save()

    def handle_action(self, action):
        if action in ['again', 'hard', 'good']:
            action_method = getattr(self, action, None)
            if callable(action_method):
                action_method()
                return
        raise ValueError(f"Invalid action: {action}")
