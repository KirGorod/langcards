# Generated by Django 4.2.6 on 2023-10-19 22:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0012_deck_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cardprogress',
            name='interval',
        ),
    ]
