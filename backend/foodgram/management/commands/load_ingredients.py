import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from foodgram.models import Ingredient


DATA_ROOT = os.path.join(settings.BASE_DIR, 'data')


class Command(BaseCommand):
    """
    Command which allows you to upload .csv file with ingredients
    For localizations purposes IngredientsEN is hardcoded
    """
    def add_arguments(self, parser):
        parser.add_argument('filename', default='ingredientsEN.csv', nargs='?',
                            type=str)

    def handle(self, *args, **options):
        try:
            with open(os.path.join(DATA_ROOT, options['filename']), 'r',
                      encoding='utf-8') as f:
                data = csv.reader(f)
                for row in data:
                    name, measurement_unit = row
                    Ingredient.objects.get_or_create(
                        name=name,
                        measurement_unit=measurement_unit
                    )
        except FileNotFoundError:
            raise CommandError('Add ingredients.csv to /data/ directory')
