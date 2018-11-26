from django.urls import reverse
from nose.tools import eq_
from rest_framework.test import APITestCase
from rest_framework import status
from faker import Faker
from places.users.test.factories import UserFactory
from places.venues.models import Favourites
from places.venues.test.factories import VenueFactory

fake = Faker()


class TestVenueListTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('venue-list')
        self.user = UserFactory()
        favourte, created = Favourites.objects.get_or_create(user_id=self.user.id)
        self.venue = VenueFactory(place_id='ChIJDQdD0ir_0YURbOpgGbZsYGk')
        favourte.venues.add(self.venue)

    def test_post_request_create_favourite_place(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        response = self.client.post(self.url, {'place_id': 'ChIJKZPady350YUROGBNDIZTUPk'})
        eq_(response.status_code, status.HTTP_200_OK)

    def test_fail_post_request_create_favourite_place_with_same_place_id(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        response = self.client.post(self.url, {'place_id': 'ChIJDQdD0ir_0YURbOpgGbZsYGk'})
        eq_(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_request_returns_a_list_of_places(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        response = self.client.get(self.url)
        eq_(response.status_code, status.HTTP_200_OK)

    def test_forbidden_whit_no_user_credentials(self):
        response = self.client.get(self.url)
        eq_(response.status_code, status.HTTP_403_FORBIDDEN)


class TestVenueDetailTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.venue = VenueFactory(place_id='ChIJDQdD0ir_0YURbOpgGbZsYGk')
        self.venue_2 = VenueFactory(place_id='ChIJKZPady350YUROGBNDIZTUPk')
        favourite, created = Favourites.objects.get_or_create(user_id=self.user.id)
        favourite.venues.add(self.venue)
        favourite.venues.add(self.venue_2)
        self.url = reverse('venue-detail', kwargs={'id': self.venue_2.id})

    def test_delete_request_favourite_vanue(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        response = self.client.delete(self.url, {})
        eq_(response.status_code, status.HTTP_200_OK)

    def test_fail_delete_request_favourite_vanue_with_no_credentials(self):
        response = self.client.delete(self.url, {})
        eq_(response.status_code, status.HTTP_403_FORBIDDEN)
