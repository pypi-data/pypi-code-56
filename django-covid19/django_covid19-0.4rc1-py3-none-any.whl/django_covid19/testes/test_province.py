from django.test import TestCase
from django.test.client import Client as DjangoClient

from django.urls import reverse

# Create your tests here.

class ProvincesTestCase(TestCase):

    fixtures = ['province.json']

    countryCode = 'USA'
    provinceCode = 'AL'
    provinceName = 'Alabama'

    def test_list_view_status_code(self):
        kwargs = {'countryCode': self.countryCode}
        url = reverse('django_covid19:province-list', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_list_daily_view_status_code(self):
        kwargs = {'countryCode': self.countryCode}
        url = reverse('django_covid19:province-list-daily', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_daily_view_status_code(self):
        kwargs = {
            'countryCode': self.countryCode,
            'provinceCode': self.provinceCode
        }
        url = reverse('django_covid19:province-daily', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_daily_by_name_view_status_code(self):
        kwargs = {
            'countryCode': self.countryCode,
            'provinceName': self.provinceName
        }
        url = reverse('django_covid19:province-daily-by-name', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_detail_view_status_code(self):
        kwargs = {
            'countryCode': self.countryCode,
            'provinceCode': self.provinceCode
        }
        url = reverse('django_covid19:province-detail', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_detail_by_nameview_status_code(self):
        kwargs = {
            'countryCode': self.countryCode,
            'provinceName': self.provinceName
        }
        url = reverse('django_covid19:province-detail-by-name', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)