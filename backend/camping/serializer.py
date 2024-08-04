from rest_framework import serializers
from buchung.models import Buchung
from campingplatz.models import Campingplatz

class CampingplatzSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campingplatz
        fields = ['name', 'address', 'customer_number']

class BuchungSerializer(serializers.ModelSerializer):
    campingplatz = CampingplatzSerializer()  # Nested serializer to include campingplatz details

    class Meta:
        model = Buchung
        fields = ['id', 'booking_number', 'campingplatz', 'status', 'abrechnungsstatus', 'price', 'commission_rate', 'total_commission', 'start_date', 'end_date']
