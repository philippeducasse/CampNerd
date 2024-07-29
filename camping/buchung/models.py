from django.db import models
from campingplatz.models import Campingplatz

class Buchung(models.Model):
    STATUS_CHOICES = [
        ('offen', 'Offen'),
        ('storniert', 'Storniert'),
        ('ohne_berechnung', 'Ohne Berechnung'),
        ('abgerechnet', 'Abgerechnet'),
        ('gutschreiben', 'Gutschreiben'),
        ('gutgeschrieben', 'Gutgeschrieben'),
    ]

    booking_number = models.CharField(max_length=255, unique=True)
    campingplatz = models.ForeignKey(Campingplatz, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='offen')
    abrechnungsstatus = models.CharField(max_length=20, choices=STATUS_CHOICES, default='offen')
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.booking_number} - {self.campingplatz.name}"

    def is_billable(self):
        return self.status == 'offen' and self.abrechnungsstatus == 'offen'

    def mark_as_billed(self):
        self.abrechnungsstatus = 'abgerechnet'
        self.save()
        # Log the change here

    def apply_credit(self):
        self.abrechnungsstatus = 'gutgeschrieben'
        self.save()