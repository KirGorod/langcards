from tqdm import tqdm
from django.core.management.base import BaseCommand

from cards.models import Deck, Card, CardAdditionalImage


class Command(BaseCommand):
    help = "Closes the specified poll for voting"
    models = [Deck, Card, CardAdditionalImage]

    def handle(self, *args, **options):
        for model in self.models:
            items = model.objects.all()
            total = items.count()

            self.stdout.write(
                f'Processing {total} instances of {model.__name__}'
            )

            for item in tqdm(items, total=total):
                item.save()

            self.stdout.write(
                self.style.SUCCESS('Successfully generated hashed images')
            )
