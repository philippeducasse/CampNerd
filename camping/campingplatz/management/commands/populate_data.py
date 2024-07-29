from django.core.management.base import BaseCommand
from campingplatz.models import Campingplatz
from buchung.models import Buchung
from django.utils import timezone
from datetime import timedelta, date
import random

class Command(BaseCommand):
    help = 'Populate database with sample data'

    Campingplatz.objects.all().delete()
    Buchung.objects.all().delete()

    def handle(self, *args, **kwargs):
        camp_sites = []
        for i in range(3):
            camping_site, created = Campingplatz.objects.get_or_create(
                name = f"Campingplatz {i + 1}",
                address = f"Adresse {i + 1}",
                customer_number = f"1000{i + 1}"
            )
            camp_sites.append(camping_site)

        for i in range(100):
            start_date = date(2024, 6, random.randint(1, 15))
            end_date = start_date + timedelta(days=random.randint(1, 10))
            camping_site = random.choice(camp_sites)
            Buchung.objects.create(
                booking_number=f'B24-{i+1:03}',
                campingplatz=camping_site,  
                status='offen',
                abrechnungsstatus='offen',
                commission_rate=random.uniform(1.0, 5.0),
                price=random.uniform(50.0, 500.0),
                start_date=start_date,
                end_date=end_date
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))