from django.core.management.base import BaseCommand
from parcels.models import ParcelType
import logging


logger = logging.getLogger('parcels')


class Command(BaseCommand):
    help = 'Initialize default ParcelType records if they do not exist'

    def handle(self, *args, **options):
        default_types = [
            {"name": "Одежда"},
            {"name": "Электроника"},
            {"name": "Разное"},
        ]

        for parcel_type in default_types:
            name = parcel_type["name"]
            if not ParcelType.objects.filter(name=name).exists():
                ParcelType.objects.create(name=name)
                logger.info(f"Created ParcelType: {name}")
                self.stdout.write(self.style.SUCCESS(f"Successfully created ParcelType: {name}"))
            else:
                logger.info(f"ParcelType already exists: {name}")
                self.stdout.write(f"ParcelType already exists: {name}")