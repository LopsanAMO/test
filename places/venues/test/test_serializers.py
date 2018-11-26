from django.test import TestCase
from django.forms.models import model_to_dict
from nose.tools import eq_, ok_
from places.venues.test.factories import VenueFactory, FavouriteFactory
from places.venues.api.v1.serializers import VenueSerializer, FavouriteSimpleSerializer


class TestVenueSerializer(TestCase):
    def setUp(self):
        self.venue_data = model_to_dict(VenueFactory.build())

    def test_serializer_with_empty_data(self):
        serializer = VenueSerializer(data={})
        eq_(serializer.is_valid(), False)

    def test_serializer_with_valid_data(self):
        serializer = VenueSerializer(data=self.venue_data)
        ok_(serializer.is_valid())


class TestFavouriteSerializer(TestCase):
    def setUp(self):
        self.favourite_data = model_to_dict(FavouriteFactory())

    def test_serializer_with_empty_data(self):
        serializer = FavouriteSimpleSerializer(data={})
        eq_(serializer.is_valid(), False)
