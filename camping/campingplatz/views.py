from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from buchung.models import Buchung
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator

class BookingListView(View):
    def get(self, request):
        bookings = Buchung.objects.all().values()
        return JsonResponse(list(bookings), safe = False)
    
@require_http_methods(["POST"])
def mark_as_billed(request, pk):
    booking = get_object_or_404(Buchung, pk=pk)
    booking.abrechnungsstatus = 'abgerechnet'
    booking.save()
    return JsonResponse({'status': 'success', 'message': 'Booking marked as billed'})