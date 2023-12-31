# Generated by Django 4.2.4 on 2023-08-27 09:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0005_alter_card_deck'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardprogress',
            name='priority',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='cardprogress',
            name='due',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='cardprogress',
            name='ease',
            field=models.DecimalField(decimal_places=2, default=1.85, max_digits=5),
        ),
    ]
