from operator import itemgetter
from django.contrib.gis.geos import Point


def get_order(obj, order=None, lat=None, lng=None):
    if order is not None and order in ['rating', 'distance', 'addition_date']:
        if order == 'distance' and lat and lng:
            distances = []
            point_1 = Point(float(lat), float(lng))
            for venue in obj:
                distances.append([venue, point_1.distance(venue.location)*100])
            distances = sorted(distances, key=itemgetter(1))
            return [x[0] for x in distances]
        elif order != 'distance':
            obj = obj.order_by('-{}'.format(order))
        else:
            obj = obj
    return obj
