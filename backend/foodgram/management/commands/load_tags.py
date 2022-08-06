import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from foodgram.models import Tag

DATA_ROOT = os.path.join(settings.BASE_DIR, 'data')


class Command(BaseCommand):
    """
    Command which allows you to upload .csv file with tags
    For localizations purposes TagsEN is hardcoded
    """
    def add_arguments(self, parser):
        parser.add_argument('filename', default='tagsEN.csv', nargs='?',
                            type=str)

    def handle(self, *args, **options):
        try:
            with open(os.path.join(DATA_ROOT, options['filename']), 'r',
                      encoding='utf-8') as f:
                data = csv.reader(f)
                for row in data:
                    Tag.objects.get_or_create(
                        name=row[0],
                        color=row[1],
                        slug=row[2]
                    )
        except FileNotFoundError:
            raise CommandError('Add tagsEN.csv to /data/ directory')
