from rest_framework import serializers
from places.venues.models import Venue, Favourites
from django.contrib.gis.geos import Point


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ('location', 'name', 'place_id', 'rating', 'addition_date', 'id')


class FavouritesSerializer(serializers.ModelSerializer):
    venues = serializers.SerializerMethodField()

    class Meta:
        model = Favourites
        fields = ('user', 'venues')
        read_only_fields = ('venues',)

    def get_venues(self, obj):
        return VenueSerializer(obj.venues.all(), many=True).data


class FavouriteSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourites
        fields = ('user', 'venues')
        read_only_fields = ('venues',)


class VenueSimpleSerializer(serializers.Serializer):
    place_id = serializers.CharField()
    name = serializers.CharField()
    geo_location = serializers.JSONField()
    vicinity = serializers.CharField()
    rating = serializers.CharField()
    distance = serializers.SerializerMethodField()

    def get_distance(self, obj):
        point_1 = Point(float(obj.lat), float(obj.lng))
        point_2 = Point(float(obj.geo_location['lat']), float(obj.geo_location['lng']))
        distance = point_1.distance(point_2)
        return distance * 100
