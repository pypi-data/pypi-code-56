from django.test import TestCase
from django.test.client import Client as DjangoClient

from django.urls import reverse

# Create your tests here.

class StatisticsTestCase(TestCase):

    """Supporting Chinese cities only."""

    fixtures = ['statistics.json']

    def test_list_view_status_code(self):
        url = reverse('django_covid19:statistics-list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_latest_view_status_code(self):
        url = reverse('django_covid19:statistics-latest')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
