from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from campingplatz.models import Campingplatz
from buchung.models import Buchung
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from datetime import datetime
import random
import json

class IndexView(TemplateView):
    template_name = 'index.html'

class BookingListView(View):
    def get(self, request):
        bookings = Buchung.objects.all().values()
        return JsonResponse(list(bookings), safe=False)

@require_http_methods(["POST"])
def mark_as_billed(request, pk):
    booking = get_object_or_404(Buchung, pk=pk)
    booking.abrechnungsstatus = 'abgerechnet'
    booking.save()
    return JsonResponse({'status': 'success', 'message': 'Booking marked as billed'})

class BillingView(View):
    def get(self, request):
        camping_sites = list(Campingplatz.objects.all().values())
        return JsonResponse(camping_sites, safe=False)

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
                commission = booking.price * commission_rate
                billing_items.append({
                    'booking_id': booking.id,
                    'amount': commission
                })
        # Here you would send billing_items to the invoicing API
        # For now, let's just simulate success
        if self.send_to_invoicing_api(billing_items):
            for booking in bookings:
                if booking.abrechnungsstatus == 'offen':
                    booking.abrechnungsstatus = 'abgerechnet'
                    booking.save()
            return JsonResponse({'status': 'success', 'message': 'Billing processed successfully'})
        return JsonResponse({'status': 'error', 'message': 'Billing failed'})

    def get_commission_rate(self, booking):
        # Implement your logic to determine the commission rate
        return random.uniform(0.01, 0.05)  # For example purposes

    def send_to_invoicing_api(self, billing_items):
        # Implement your API call to the invoicing service
        return True  # Simulating a successful API call
