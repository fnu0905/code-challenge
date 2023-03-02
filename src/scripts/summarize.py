from tqdm import tqdm
from django.db.models import Avg, Sum
from app.models import WeatherRecord, WeatherSummary


def run():
    # Loop over each year from 1985 to 2014
    for year in tqdm(range(1985, 2015)):
        # Loop over each weather station
        for station in WeatherRecord.objects.values('station_id').distinct():
            station_id = station['station_id']

            # Calculate the average maximum temperature for the year and station
            avg_max_temp = WeatherRecord.objects.filter(station_id=station_id, date__year=year,
                                                        max_temp__isnull=False).aggregate(avg_max_temp=Avg('max_temp'))['avg_max_temp']

            # Calculate the average minimum temperature for the year and station
            avg_min_temp = WeatherRecord.objects.filter(station_id=station_id, date__year=year,
                                                        min_temp__isnull=False).aggregate(avg_min_temp=Avg('min_temp'))['avg_min_temp']

            # Calculate the total precipitation for the year and station
            total_precipitation = WeatherRecord.objects.filter(station_id=station_id, date__year=year,
                                                               precipitation__isnull=False).aggregate(total_precipitation=Sum('precipitation'))['total_precipitation']

            # Create a new WeatherStatistics object and save it to the database
            stats = WeatherSummary(year=year, station_id=station_id, avg_max_temp=avg_max_temp,
                                   avg_min_temp=avg_min_temp, total_precipitation=total_precipitation)
            stats.save()
