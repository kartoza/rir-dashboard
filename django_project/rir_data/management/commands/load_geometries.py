from django.core.management.base import BaseCommand
from rir_data.fixtures.somalia import administrative as somalia


class Command(BaseCommand):
    """
    Export all geometries
    """

    def handle(self, *args, **options):
        somalia.run()
