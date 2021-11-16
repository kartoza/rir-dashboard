from django.conf.urls import url
from django.urls import include
from rir_data.api.geometry import GeometryGeojsonAPI
from rir_data.api.indicator import (
    IndicatorsList, IndicatorValuesGeojson, IndicatorValues,
    IndicatorValuesByGeometry
)
from rir_dashboard.views.instances import InstancesView

geometry_api = [
    url(
        r'^(?P<geometry_level>.+)/(?P<date>.+).geojson',
        GeometryGeojsonAPI.as_view(), name='geometry-geojson-api'
    ),
]
indicator_api = [
    url(
        r'^(?P<pk>\d+)/values/by-geometry/(?P<geometry_pk>\d+)/',
        IndicatorValuesByGeometry.as_view(), name='indicator-values-by-geometry'),
    url(
        r'^(?P<pk>\d+)/values/(?P<geometry_identifier>.+)/(?P<geometry_level>.+)/(?P<date>.+).geojson',
        IndicatorValuesGeojson.as_view(), name='indicator-values-geojson-api'),
    url(
        r'^(?P<pk>\d+)/values/(?P<geometry_identifier>.+)/(?P<geometry_level>.+)/(?P<date>.+)',
        IndicatorValues.as_view(), name='indicator_values-api'),
    url(r'^', IndicatorsList.as_view(), name='indicator-list-api'),
]
api = [
    url(r'^geometry/', include(geometry_api)),
    url(r'^indicator/', include(indicator_api)),
]

instance_url = [
    url(r'^api/', include(api)),
    url(r'^', include('rir_dashboard.urls')),
]

urlpatterns = [
    url(r'^(?P<slug>[^/]+)/', include(instance_url)),
    url(r'^', InstancesView.as_view(), name='instances-view'),
]
