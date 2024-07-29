from django.urls import path
from . import views

urlpatterns = [
    path('bookings/', views.BookingListView.as_view(), name = 'booking-list'),
    path('bookings/<int:pk>/mark_as_billed/', views.mark_as_billed, name = 'mark_as_billed')
]