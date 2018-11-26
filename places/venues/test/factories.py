import factory
from factory.fuzzy import FuzzyFloat
from places.venues.test.utils import FuzzyPoint
from places.users.test.factories import UserFactory
from places.venues.models import Venue, Favourites


class VenueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Venue
        django_get_or_create = ('location', 'place_id')

    location = FuzzyPoint()
    name = factory.Sequence(lambda n: f'testnamevenue{n}')
    place_id = factory.Sequence(lambda n: f'testplacevenueid{n}')
    rating = FuzzyFloat(0, 5)


class FavouriteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Favourites

    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def venues(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for venue in extracted:
                self.venues.add(venue)
