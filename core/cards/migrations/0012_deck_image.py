# Generated by Django 4.2.5 on 2023-10-12 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0011_alter_cardprogress_interval_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='deck',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='decks/'),
        ),
    ]
