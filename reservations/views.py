# -*- coding: utf-8 -*-
from rest_framework import generics
from .serializers import ReservationSerializer
from .models import Reservation
import datetime
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

class CreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
        serializer.save()


class DetailsView(generics.RetrieveUpdateAPIView):
    """This class handles the http GET and PUT requests."""
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def put(self, request, *args, **kwargs):
        if "state" in self.request.data:
            # Dont allow too frequent change of state value
            if self.queryset[0]._state_modified and self.queryset[0]._state_modified > timezone.now() - datetime.timedelta(seconds=15):
                return Response(status=status.HTTP_403_FORBIDDEN)
            #on state change, save last modified time
            self.request.data['_state_modified'] = timezone.now()
        return self.partial_update(request, *args, **kwargs)
