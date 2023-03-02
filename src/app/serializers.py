from rest_framework import serializers
from app.models import WeatherRecord, WeatherSummary


class WeatherRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherRecord
        fields = '__all__'


class WeatherSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherSummary
        fields = '__all__'
