from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from datetime import datetime
from decimal import Decimal
from .models import Campingplatz
from buchung.models import Buchung, ChangeLog
import json
import random

class BookingListView(View):
    def get(self, request):
        bookings = Buchung.objects.all().values()
        return JsonResponse(list(bookings), safe=False)

@require_http_methods(["POST"])
#@login_required
def mark_as_billed(request, pk):
    booking = get_object_or_404(Buchung, pk=pk)
    old_value = booking.abrechnungsstatus
    booking.abrechnungsstatus = 'abgerechnet'
    booking.save()
    log_change('test_user', booking, 'abrechnungsstatus', old_value, 'abgerechnet')
    return JsonResponse({'status': 'success', 'message': 'Booking marked as billed'})

@require_http_methods(["POST"])
#@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Buchung, pk=pk)
    old_value = booking.abrechnungsstatus
    booking.abrechnungsstatus = 'storniert'
    booking.save()
    log_change('test_user', booking, 'abrechnungsstatus', old_value, 'storniert')
    return JsonResponse({'status': 'success', 'message': 'Booking canceled'})

@require_http_methods(["POST"])
#@login_required
def credit_booking(request, pk):
    booking = get_object_or_404(Buchung, pk=pk)
    old_value = booking.abrechnungsstatus
    booking.abrechnungsstatus = 'gutschreiben'
    booking.save()
    log_change('test_user', booking, 'abrechnungsstatus', old_value, 'gutschreiben')
    return JsonResponse({'status': 'success', 'message': 'Booking credited'})

@require_http_methods(["POST"])
#@login_required
def update_commission_rate(request, pk):
    booking = get_object_or_404(Buchung, pk=pk)
    data = json.loads(request.body)
    old_value = booking.commission_rate
    new_value = Decimal(data.get('commission_rate'))
    booking.commission_rate = new_value
    booking.save()
    log_change('test_user', booking, 'commission_rate', str(old_value), str(new_value))
    return JsonResponse({'status': 'success', 'message': 'Commission rate updated'})

def log_change(user, booking, field_changed, old_value, new_value):
    ChangeLog.objects.create(
        booking=booking,
        user=user,
        field_changed=field_changed,
        old_value=old_value,
        new_value=new_value,
        date=datetime.now()
    )

class CampingSitesView(View):
    def get(self, request):
        camping_sites = list(Campingplatz.objects.all().values())
        return JsonResponse(camping_sites, safe=False)

class BillingView(View):
    @method_decorator(login_required)
    def post(self, request):
        data = json.loads(request.body)
        camping_site_id = data.get('camping_site')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        camping_site = get_object_or_404(Campingplatz, id=camping_site_id)
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        bookings = Buchung.objects.filter(campingplatz=camping_site, start_date__gte=start_date, end_date__lte=end_date)
        return self.process_bookings(bookings, camping_site)

    def process_bookings(self, bookings, camping_site):
        billing_items = []
        for booking in bookings:
            if booking.abrechnungsstatus == 'offen':
                commission_rate = self.get_commission_rate(booking)
                commission = booking.price * Decimal(commission_rate)  # Ensure consistent use of Decimal
                billing_items.append({
                    'booking_id': booking.id,
                    'amount': commission
                })
        # Here you would send billing_items to the invoicing API
        # For now, let's just simulate success
        if self.send_to_invoicing_api(billing_items):
            for booking in bookings:
                if booking.abrechnungsstatus == 'offen':
                    old_value = booking.abrechnungsstatus
                    booking.abrechnungsstatus = 'abgerechnet'
                    booking.save()
                    log_change('test_user', booking, 'abrechnungsstatus', old_value, 'abgerechnet')
            return JsonResponse({'status': 'success', 'message': 'Billing processed successfully'})
        return JsonResponse({'status': 'error', 'message': 'Billing failed'})

    def get_commission_rate(self, booking):
        # Implement your logic to determine the commission rate
        return random.uniform(0.01, 0.05)  # For example purposes

    def send_to_invoicing_api(self, billing_items):
        # Implement your API call to the invoicing service
        return True  # Simulating a successful API call
