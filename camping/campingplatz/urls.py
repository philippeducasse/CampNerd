from django.urls import path
from . import views
from buchung.models import ChangeLog

urlpatterns = [
    path('billing/', views.BillingView.as_view(), name='billing'),
    path('camping_sites/', views.CampingSitesView.as_view(), name='camping_sites'),
    path('bookings/<int:pk>/create_invoice/', views.CreateInvoiceView.as_view(), name='create_invoice'),
    path('bookings/', views.BookingListView.as_view(), name = 'booking-list'),
    path('bookings/<int:pk>/mark_as_billed/', views.mark_as_billed, name = 'mark_as_billed'),
    path('bookings/<int:pk>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('bookings/<int:pk>/credit/', views.credit_booking, name='credit_booking'),
    path('bookings/<int:pk>/update_commission_rate/', views.update_commission_rate, name='update_commission_rate'),
    path('bookings/<int:pk>/logs/', ChangeLog.view_logs, name='view_logs'),
]