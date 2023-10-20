from decimal import Decimal

from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class Deck(models.Model):
    title = models.CharField(max_length=255)
    default = models.BooleanField('Default Deck', default=False)
    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    image = models.ImageField(upload_to='decks/', blank=True, null=True)
    image_hash = models.CharField(max_length=500, null=True, blank=True)

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
    image_hash = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f'{self.word} | {self.translation}'


class CardAdditionalImage(models.Model):
    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name='additional_images'
    )
    image = models.ImageField(upload_to='cards_additional/')
    image_hash = models.CharField(max_length=500, null=True, blank=True)


class CardProgressManager(models.Manager):
    def pop_card(self, user, deck):
        """
        Get first card to learn
        """
        return self.filter(
            user=user,
            card__deck=deck,
            due__lte=timezone.now()
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
    DEFAULT_EASE = 1.85
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
    ease = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=DEFAULT_EASE
    )
    priority = models.PositiveIntegerField(default=1)
    objects = CardProgressManager()

    def __str__(self):
        return f'{self.user.username}`s progress for card {self.card.word}'

    def again(self):
        interval = 0
        ease = max(self.ease - Decimal('0.25'), self.DEFAULT_EASE)
        priority = self.priority + 1
        self._update_progress(interval, priority=priority, new_ease=ease)

    def hard(self):
        interval = 0
        ease = max(self.ease - Decimal('0.15'), self.DEFAULT_EASE)
        priority = self.priority + 2
        self._update_progress(interval, priority=priority, new_ease=ease)

    def good(self):
        interval = 0
        ease = self.ease + Decimal('0.15')
        priority = self.priority + 3

        if self.stage == self.RELEARNING:
            interval = 1
        if self.stage == self.LEARNING:
            interval = 2
        if self.stage == self.REVIEW:
            interval = 3
            ease = self.ease + Decimal('0.25')

        self._update_progress(interval, priority=priority, new_ease=ease)

    def _update_progress(self, interval, priority, new_ease):
        days_2 = 2
        days_6 = 6
        self.ease = new_ease
        learning_threshold = self.ease > days_2
        review_threshold = interval * self.ease > days_6

        if self.stage == self.NEW and learning_threshold:
            self.stage = self.LEARNING
            interval = 1

        if self.stage == self.LEARNING and review_threshold:
            self.stage = self.REVIEW

        days = int(interval * self.ease)
        self.due = (timezone.now() + timedelta(days=days)).date()
        self.priority = priority
        if self.due > timezone.now().date():
            self.store_log(self.user, self.card)
            self.priority = 1

        self.save()

    def handle_action(self, action):
        if action in ['again', 'hard', 'good']:
            action_method = getattr(self, action, None)
            if callable(action_method):
                action_method()
                return
        raise ValueError(f"Invalid action: {action}")

    def store_log(self, user, card):
        LearningLog.objects.create(user=user, card=card)


class LearningLog(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='learning_log'
    )
    card = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
