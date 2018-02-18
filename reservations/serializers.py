from rest_framework import serializers
from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    state = serializers.IntegerField(required=False)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""

        model = Reservation
        fields = ['state','arrival_date', 'guest_name', 'room_type', 'hotel_name', 'departure_date', '_state_modified']
        extra_kwargs = {'_state_modified': {'write_only': True}}
