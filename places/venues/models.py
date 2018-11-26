from django.db import models
from django.contrib.gis.db import models as gismodel
from places.users.models import User


class Venue(gismodel.Model):
    location = gismodel.PointField(unique=True)
    name = gismodel.CharField(max_length=200)
    place_id = gismodel.CharField(max_length=110, unique=True)
    rating = gismodel.FloatField(null=True, blank=True)
    addition_date = gismodel.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name

    def to_json(self):
        return {
            'location': self.location,
            'name': self.name,
            'place_id': self.place_id,
            'rating': self.rating,
            'addition_data': self.addition_date
        }


class Favourites(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    venues = models.ManyToManyField(Venue, blank=True)

    def __str__(self):
        return "favourite venues of {}".format(self.user.username)

    def to_json(self):
        return {
            'user': self.user.id,
            'venues': [x.to_json() for x in self.venues.all()]
        }
