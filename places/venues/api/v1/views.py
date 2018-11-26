from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from django.conf import settings
from django.core.cache import cache
from django.contrib.gis.geos import Point
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from places.users.permissions import IsUserOrReadOnly
from rest_framework.permissions import IsAuthenticated
from places.venues.api.v1.serializers import VenueSimpleSerializer, VenueSerializer
from places.venues.api.v1.utils import get_venues, get_venue_detail
from places.venues.api.v1.filters import get_order
from places.venues.models import Favourites, Venue


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class VenuesSearchViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = VenueSimpleSerializer
    queryset = {}

    @action(detail=False, methods=['GET'], permission_classes=[IsUserOrReadOnly])
    def places(self, request):
        """Get places nearby, by name

        :param lat: (float) required
        :param lng: (float) required
        :param query: (str) could be empty
        :param order: (str) could be empty or distance or prominence
        :return: list of places
        """
        lat, lng = self.request.query_params.get('lat', None), self.request.query_params.get('lng', None)
        query = self.request.query_params.get('query', '')
        order = self.request.query_params.get('order', None)
        if lat is not None and lng is not None:
            if order not in ['distance', 'prominence']:
                order = None
            cache_data = self.get_cache(query, lat, lng)
            if cache_data is not None and cache_data is not False and len(cache_data) > 10:
                r = cache_data
            else:
                r = get_venues(lat, lng, query, order)
                if r is False:
                    return Response(status=r.status_code)
                self.set_cache(query, r)
            page = self.paginate_queryset(r)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(r, many=True)
            return Response(serializer.data)
        return Response(status=400, data={'detail': 'lat and lng params are required'})

    def get_cache(self, query, lat, lng, radius=True):
        """"Get cache places by query
        :param query: (str) required
        :param lat: (float) could be empty only if radius is True
        :param lng: (float) could be empty only if radius is True
        :param radius: (bool)
        :return: False
        """
        cache_data = cache.get(query)
        if cache_data is not None:
            if radius:
                for place in cache_data:
                    point = Point(float(lat), float(lng))
                    place.distance = point.distance(Point(
                        float(place.geo_location['lat']),
                        float(place.geo_location['lng']))
                    ) * 100
                return [place for place in cache_data if place.distance <= 5]
            else:
                return cache_data
        else:
            return False

    def set_cache(self, query, results):
        """

        :param query: (str) required
        :param results: (list) list of places
        :return: empty
        """
        cache_data = self.get_cache(query, None, None, False)
        if cache_data is None or cache_data is False:
            cache.set(query, results, timeout=None)
        else:
            filtered_results = filter(lambda x: x.place_id not in [y.place_id for y in cache_data], results)
            to_cached = cache_data + list(filtered_results)
            cache.set(query, to_cached, timeout=None)


# TODO quitar lo del get_alterno_object y no rewritin el destroy


class FavouriteVenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'
    lookup_value_regex = '[0-9]'

    def get_altern_object(self):
        try:
            return Venue.objects.get(id=self.kwargs['id'])
        except Exception:
            return False

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        r = get_venue_detail(request.data.get('place_id'))
        if r is False:
            return Response(status=400, data={'place not found'})
        serializer = VenueSerializer(data=r.__dict__)
        if serializer.is_valid():
            serializer.save()
            favourites, created = Favourites.objects.get_or_create(user=request.user)
            favourites.venues.add(serializer.instance)
            favourites.save()
        else:
            return Response(status=400, data=serializer.errors)
        return Response(status=200, data={'detail': 'created'})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_altern_object()
        if instance is False:
            return Response(status=404, data={'detail': 'venue not found'})
        self.perform_destroy(instance)
        return Response(status=200, data={'detail': 'deleted'})

    def get_queryset(self):
        fav, created = Favourites.objects.get_or_create(user=self.request.user)
        venues = Venue.objects.filter(id__in=fav.venues.all())
        params = self.request.query_params
        order = params.get('order', None)
        lat, lng = params.get('lat', None), params.get('lng', None)
        venues = get_order(venues, order, lat, lng)
        return venues


