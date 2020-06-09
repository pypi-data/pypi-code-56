from django.test import TestCase
from django.test.client import Client as DjangoClient

from django.urls import reverse

# Create your tests here.

class CountriesTestCase(TestCase):

    fixtures = ['country.json']
    countryCode = 'USA'

    def test_list_view_status_code(self):
        url = reverse('django_covid19:country-list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        for item in response.json():
            self.assertEquals('countryCode' in item, True)
            self.assertEquals('countryName' in item, True)
            self.assertEquals('continents' in item, True)

    def test_list_daily_view_status_code(self):
        url = reverse('django_covid19:country-list-daily')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_detail_view_status_code(self):
        kwargs = {'countryCode': self.countryCode}
        url = reverse('django_covid19:country-detail', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_daily_view_status_code(self):
        kwargs = {'countryCode': self.countryCode}
        url = reverse('django_covid19:country-daily', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)