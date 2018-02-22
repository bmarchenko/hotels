from rest_framework import serializers
from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    state = serializers.IntegerField(required=False)

    def validate(self, data):
        #arrival_date must be =< departure_date
        if 'departure_date' in data or 'arrival_date' in data:
            departure_date = data.get('departure_date', getattr(self.instance, 'departure_date', None))
            arrival_date = data.get('arrival_date', getattr(self.instance, 'arrival_date', None))
            if arrival_date > departure_date:
                raise serializers.ValidationError("Departure must occur after arrival")
        return data

    class Meta:
        """Meta class to map serializer's fields with the model fields."""

        model = Reservation
        fields = ['state','arrival_date', 'guest_name', 'room_type', 'hotel_name', 'departure_date', '_state_modified']
        extra_kwargs = {'_state_modified': {'write_only': True}}
