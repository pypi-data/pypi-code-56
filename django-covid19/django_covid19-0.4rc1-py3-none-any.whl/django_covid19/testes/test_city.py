from django.test import TestCase
from django.test.client import Client as DjangoClient

from django.urls import reverse

# Create your tests here.

class CitiesTestCase(TestCase):

    """Supporting Chinese cities only."""

    fixtures = ['city.json']

    countryCode = 'CHN'
    cityName = '深圳'

    def test_list_view_status_code(self):
        kwargs = {'countryCode': self.countryCode,}
        url = reverse('django_covid19:city-list', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_detail_view_status_code(self):
        kwargs = {
            'countryCode': self.countryCode,
            'cityName': self.cityName
        }
        url = reverse('django_covid19:city-detail', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
