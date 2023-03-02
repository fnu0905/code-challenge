from django.urls import path
from rest_framework import pagination
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import WeatherRecord, WeatherSummary
from .serializers import WeatherRecordSerializer, WeatherSummarySerializer


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


@swagger_auto_schema(methods=['get'], manual_parameters=[openapi.Parameter('date', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False), openapi.Parameter('station_id', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False)], responses={200: WeatherRecordSerializer(many=True)})
@api_view(['GET'])
def weather_list(request):
    queryset = WeatherRecord.objects.all().order_by('date', 'station_id')

    # Filter by date
    date = request.query_params.get('date', None)
    if date is not None:
        queryset = queryset.filter(date=date)

    # Filter by station ID
    station_id = request.query_params.get('station_id', None)
    if station_id is not None:
        queryset = queryset.filter(station_id=station_id)

    # Paginate the results
    paginator = StandardResultsSetPagination()
    paginated_queryset = paginator.paginate_queryset(queryset, request)

    serializer = WeatherRecordSerializer(paginated_queryset, many=True)
    return paginator.get_paginated_response(serializer.data)


@swagger_auto_schema(methods=['get'], manual_parameters=[openapi.Parameter('year', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=False), openapi.Parameter('station_id', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False)], responses={200: WeatherSummarySerializer(many=True)})
@api_view(['GET'])
def weather_summary_list(request):
    queryset = WeatherSummary.objects.all().order_by('year', 'station_id')

    # Filter by year
    year = request.query_params.get('year', None)
    if year is not None:
        queryset = queryset.filter(year=year)

    # Filter by station ID
    station_id = request.query_params.get('station_id', None)
    if station_id is not None:
        queryset = queryset.filter(station_id=station_id)

    # Paginate the results
    paginator = StandardResultsSetPagination()
    paginated_queryset = paginator.paginate_queryset(queryset, request)

    serializer = WeatherSummarySerializer(paginated_queryset, many=True)
    return paginator.get_paginated_response(serializer.data)
