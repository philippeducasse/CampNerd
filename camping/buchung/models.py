from django.db import models
from campingplatz.models import Campingplatz
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

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
        # ADD LOGGING
        #For this purpose, the changed values, the date and the operator are saved.

    def apply_credit(self):
        self.abrechnungsstatus = 'gutgeschrieben'
        self.save()


class ChangeLog(models.Model):
    booking = models.ForeignKey(Buchung, on_delete=models.CASCADE)
    user = models.CharField(max_length=255)
    field_changed = models.CharField(max_length=255)
    old_value = models.CharField(max_length=255)
    new_value = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.booking.booking_number} - {self.field_changed}"
    
    @require_http_methods(["GET"])
    def view_logs(request, pk):
        logs = ChangeLog.objects.filter(booking_id=pk).values()
        return JsonResponse(list(logs), safe=False)