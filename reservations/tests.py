# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
from django.test import TestCase
from reservations.models import Reservation
from reservations.constants import STANDARD, FUTURE, CHECKEDOUT, INHOUSE
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse

test_reservation_dict = dict(guest_name="John Doe",
                           arrival_date="2018-01-01",
                           departure_date="2018-01-02",
                           hotel_name="Intercontinental",
                           room_type=STANDARD)


class ModelTestCase(TestCase):
    """This class defines the test suite for the reservation model."""

    def setUp(self):
        self.reservation = Reservation(**test_reservation_dict)

    def test_model_can_create_a_reservation(self):
        """Test the reservation model can create a reservation."""
        old_count = Reservation.objects.count()
        self.reservation.save()
        new_count = Reservation.objects.count()
        self.assertNotEqual(old_count, new_count)


class ViewTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.response = self.client.post(
            reverse('create'),
            test_reservation_dict,
            format="json")
        self.reservation = Reservation.objects.get()

    def test_api_can_create_reservation(self):
        """Test the api has bucket creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 1)


    def test_api_can_get_a_reservation(self):
        """Test the api can get a given reservation."""
        response = self.client.get(
            reverse('details',
            kwargs={'pk': self.reservation.id}), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #state must be in the past
        test_reservation_dict['state'] = CHECKEDOUT
        self.assertEqual(response.data, test_reservation_dict)


    def test_api_forbids_too_often_update_state(self):
        """Test the api can update a given reservation."""
        #Attepmt #1
        dc = {'state': INHOUSE}
        res = self.client.put(
            reverse('details', kwargs={'pk': self.reservation.id}),
            dc, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['state'], INHOUSE)

        # Attepmt #2, should be failed
        dc = {'state': CHECKEDOUT}
        res = self.client.put(
            reverse('details', kwargs={'pk': self.reservation.id}),
            dc, format='json'
        )
        #too often change of state field is forbidden
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Reservation.objects.first().state, INHOUSE)

        #Attepmt #3 wait 15 seconds and try again, should work
        time.sleep(15)
        res = self.client.put(
            reverse('details', kwargs={'pk': self.reservation.id}),
            dc, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Reservation.objects.first().state, CHECKEDOUT)

