from django.contrib import admin
from places.venues.models import Venue, Favourites


admin.site.register(Venue)
admin.site.register(Favourites)