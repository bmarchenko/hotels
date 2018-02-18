# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import DateRangeField
import datetime
from reservations.constants import ROOM_CHOICES, STATES_CHOICES, FUTURE, CHECKEDOUT, INHOUSE

#TODO: implement Hotels model
# class Hotel(models.Model):
#     """
#     Common hotel information
#     """
#     name = models.CharField(max_length=300)
#     rooms_available = models.BooleanField(default=True)


class Reservation(models.Model):
    """
    This class represents Hotel resevation model
    """
    guest_name = models.CharField(max_length=300, null=True, blank=True)
    arrival_date = models.DateField()
    departure_date = models.DateField()
    # dates = DateRangeField()
    hotel_name = models.CharField(max_length=300)
    room_type = models.IntegerField(choices=ROOM_CHOICES)
    _status = models.IntegerField(choices=STATES_CHOICES, help_text="service field for state property", null=True, blank=True)
    _state_modified = models.DateTimeField(null=True, blank=True, help_text="just in order to track when the last time of state change")

    def get_state(self):
        if self._status:
            #if set explicitly, return
            return self._status
        else:
            if self.arrival_date > datetime.date.today():
                return FUTURE
            #TODO: make sure arrival_date < departure_date
            elif self.arrival_date < datetime.date.today() < self.departure_date:
                return INHOUSE
            else:
                return CHECKEDOUT

    def set_state(self, value):
        self._status = value

    state = property(get_state, set_state)

    def __str__(self):
        return "{} {} {}".format(self.hotel_name, self.guest_name, self.arrival_date)