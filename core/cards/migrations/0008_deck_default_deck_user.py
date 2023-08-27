# Generated by Django 4.2.4 on 2023-08-27 09:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cards', '0007_card_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='deck',
            name='default',
            field=models.BooleanField(default=False, verbose_name='Default Deck'),
        ),
        migrations.AddField(
            model_name='deck',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]