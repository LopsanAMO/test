import requests
import json
from django.conf import settings
from django.contrib.gis.geos import Point


class Place(object):
    place_id = None
    name = None
    location = None
    geo_location = None
    vicinity = None
    distance = None
    rating = None
    lat = None
    lng = None

    def __init__(self, obj, lat=None, lng=None):
        self.place_id = obj['place_id']
        self.name = obj['name']
        self.geo_location = obj['geometry']['location']
        self.vicinity = obj['vicinity']
        self.rating = obj.get('rating', '')
        self.lat = lat
        self.lng = lng
        self.location = Point(obj['geometry']['location']['lat'], obj['geometry']['location']['lng'])


def get_venues(lat, lng, query, order=None):
    base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
    search_url = '&location={},{}&keyword={}&key={}'.format(lat, lng, query, settings.GOOGLE_API_KEY)
    if order is not None and order != 'prominence':
        base_url += 'rankby={}'.format(order)
    else:
        base_url += 'radius=3200&rankby=prominence'
    r = requests.get(url=base_url+search_url)
    if r.status_code != 200:
        return False
    res = json.loads(r.text)
    venues_list = []
    for venue in res['results']:
        venues_list.append(Place(venue, lat, lng))
    return venues_list


def get_venue_detail(place_id):
    base_url = 'https://maps.googleapis.com/maps/api/place/details/json?placeid={}&key={}'.format(
        place_id, settings.GOOGLE_API_KEY
    )
    r = requests.get(url=base_url)
    if r.status_code != 200:
        return False
    res = json.loads(r.text)
    return Place(res['result'])
