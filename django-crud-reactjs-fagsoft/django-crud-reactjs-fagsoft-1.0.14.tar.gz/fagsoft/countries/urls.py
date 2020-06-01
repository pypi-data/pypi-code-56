from rest_framework import routers
from fagsoft.countries.views import (
    CountryViewSet,
    StateViewSet,
    CityViewSet
)

router = routers.DefaultRouter()
router.register('countries', CountryViewSet)
router.register('countries_states', StateViewSet)
router.register('countries_cities', CityViewSet)
