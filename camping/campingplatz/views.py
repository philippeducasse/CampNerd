from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from decimal import Decimal
from .models import Campingplatz
from buchung.models import Buchung, ChangeLog
import json
import random

class BookingListView(View):
      def get(self, request):
        camping_site_id = request.GET.get('camping_site')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        # Log the received parameters
        print(f"Received parameters: camping_site_id={camping_site_id}, start_date={start_date}, end_date={end_date}")

        if camping_site_id and start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                return JsonResponse({'error': 'Invalid date format'}, status=400)

            bookings = Buchung.objects.filter(
                campingplatz_id=camping_site_id,
                start_date__gte=start_date,
                end_date__lte=end_date
            ).values()
        else:
            bookings = Buchung.objects.all().values()

        # Log the number of bookings found
        print(f"Found {len(bookings)} bookings")

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
                booking.commission_rate = commission_rate  
                booking.save() 
                billing_items.append({
                    'booking_id': booking.id,
                    'amount': booking.total_commission
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
    

@method_decorator(csrf_exempt, name='dispatch')
class CreateInvoiceView(View):
    def post(self, request, pk):
        booking = get_object_or_404(Buchung, pk=pk)
        invoice_data = self.generate_invoice_data(booking)

        # Simulate sending the invoice data to the billing software API
        response = self.send_invoice_to_api(invoice_data)

        if response:
            booking.abrechnungsstatus = 'abgerechnet'
            booking.save()
            return JsonResponse({'status': 'success', 'message': 'Invoice created and sent successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to create and send invoice'})

    def generate_invoice_data(self, booking):
        # Generate the invoice data in the required export format
        return {
            'booking_id': str(booking.id),
            'booking_number': booking.booking_number,
            'price': float(booking.price),
            'commission_rate': float(booking.commission_rate) if booking.commission_rate is not None else None,
            'total_commission': float(booking.total_commission) if booking.total_commission is not None else None,
            'customer_name': f"{booking.campingplatz.name}",
            'departure_date': booking.end_date.strftime('%Y-%m-%d'),
            # Add other required fields
        }

    def send_invoice_to_api(self, invoice_data):
        # Implement the actual API call to the billing software here
        # Simulating a successful API call
        print(f"Sending invoice data to API: {json.dumps(invoice_data)}")
        return True
