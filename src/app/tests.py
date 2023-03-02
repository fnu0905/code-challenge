from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from datetime import date
from .models import WeatherRecord, WeatherSummary


class WeatherRecordTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        WeatherRecord.objects.create(
            station_id=1234,
            date=date(2000, 1, 1),
            max_temp=20,
            min_temp=10,
            precipitation=5,
        )
        WeatherRecord.objects.create(
            station_id=1234,
            date=date(2000, 1, 2),
            max_temp=15,
            min_temp=5,
            precipitation=10,
        )

    def test_get_all_weather_records(self):
        response = self.client.get(reverse("weather-record-list"))
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_filtered_weather_records(self):
        response = self.client.get(
            reverse("weather-record-list") + "?station_id=1234&date=2000-01-01")
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]["station_id"], '1234')
        self.assertEqual(response.data['results'][0]["date"], "2000-01-01")
        self.assertEqual(response.data['results'][0]["max_temp"], '20.0')
        self.assertEqual(response.data['results'][0]["min_temp"], '10.0')
        self.assertEqual(response.data['results'][0]["precipitation"], '5.0')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WeatherSummaryTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        WeatherRecord.objects.create(
            station_id=1234,
            date=date(2000, 1, 1),
            max_temp=20,
            min_temp=10,
            precipitation=5,
        )
        WeatherRecord.objects.create(
            station_id=1234,
            date=date(2000, 1, 2),
            max_temp=15,
            min_temp=5,
            precipitation=10,
        )
        WeatherSummary.objects.create(
            station_id=1234,
            year=2000,
            avg_max_temp=17.5,
            avg_min_temp=7.5,
            total_precipitation=15,
        )

    def test_get_all_weather_stats(self):
        response = self.client.get(reverse("weather-summary-list"))
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_filtered_weather_stats(self):
        response = self.client.get(
            reverse("weather-summary-list") + "?station_id=1234")
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]["station_id"], '1234')
        self.assertEqual(response.data['results'][0]["year"], 2000)
        self.assertEqual(response.data['results'][0]["avg_max_temp"], '17.5')
        self.assertEqual(response.data['results'][0]["avg_min_temp"], '7.5')
        self.assertEqual(response.data['results'][0]["total_precipitation"], '15.0')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
