from django.conf.urls import url
from django.urls import include
from rir_data.api.indicator import (
    IndicatorsList, IndicatorValuesGeojson, IndicatorValues
)

indicator_api = [

    url(
        r'^(?P<pk>\d+)/values/(?P<geometry_identifier>.+)/(?P<geometry_level>.+)/(?P<date>.+).geojson',
        IndicatorValuesGeojson.as_view(), name='indicator-values-geojson'),
    url(
        r'^(?P<pk>\d+)/values/(?P<geometry_identifier>.+)/(?P<geometry_level>.+)/(?P<date>.+)',
        IndicatorValues.as_view(), name='indicator_values'),
    url(r'^', IndicatorsList.as_view(), name='indicator-list'),
]
api = [
    url(r'^indicator/', include(indicator_api))
]

instance_url = [
    url(r'^api/', include(api)),
    url(r'^', include('rir_dashboard.urls')),
]

urlpatterns = [
    url(r'^(?P<slug>[^/]+)/', include(instance_url)),
]
