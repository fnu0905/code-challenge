from django.urls import path
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from .views import weather_list, weather_summary_list


schema_view = get_schema_view(
    openapi.Info(
        title="Weather API",
        default_version='v1',
        description="API for weather data",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('weather/', weather_list, name='weather-record-list'),
    path('weather/stats/', weather_summary_list, name='weather-summary-list'),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
]
