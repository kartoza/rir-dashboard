from django.conf.urls import url
from django.urls import include
from rir_data.api.download import DownloadMasterData, DownloadMasterDataCheck
from rir_data.api.geometry import GeometryGeojsonAPI, GeometryDetailAPI
from rir_data.api.indicator import (
    IndicatorsList, IndicatorValues, IndicatorValuesByGeometryAndLevel, IndicatorValuesByDateAndGeojson, IndicatorValuesByDate,
    IndicatorValuesByGeometry, IndicatorReportingUnits
)
from rir_data.api.indicators import IndicatorsValuesByGeometryDate
from rir_dashboard.views.instances import InstancesView

geometry_api = [
    url(
        r'^(?P<geometry_level>.+)/(?P<date>.+).geojson',
        GeometryGeojsonAPI.as_view(), name='geometry-geojson-api'
    ),
    url(
        r'^(?P<pk>.+)',
        GeometryDetailAPI.as_view(), name='geometry-detail-api'
    ),
]
indicator_api = [
    url(
        r'^(?P<pk>\d+)/values/by-geometry/(?P<geometry_pk>\d+)/',
        IndicatorValuesByGeometry.as_view(), name='indicator-values-by-geometry'
    ),
    url(
        r'^(?P<pk>\d+)/values/(?P<geometry_identifier>.+)/(?P<geometry_level>.+)/(?P<date>.+).geojson',
        IndicatorValuesByDateAndGeojson.as_view(), name='indicator-values-by-date-geojson-api'
    ),
    url(
        r'^(?P<pk>\d+)/values/(?P<geometry_identifier>.+)/(?P<geometry_level>.+)/(?P<date>.+)',
        IndicatorValuesByDate.as_view(), name='indicator-values-by-date-api'
    ),
    url(
        r'^(?P<pk>\d+)/values/(?P<geometry_identifier>.+)/(?P<geometry_level>.+)',
        IndicatorValuesByGeometryAndLevel.as_view(), name='indicator-values-by-geometry-and-level-api'
    ),
    url(
        r'^(?P<pk>\d+)/values',
        IndicatorValues.as_view(), name='indicator-values-api'
    ),
    url(
        r'^(?P<pk>\d+)/reporting-units',
        IndicatorReportingUnits.as_view(), name='indicator-reporting-units-api'
    ),
    url(r'^', IndicatorsList.as_view(), name='indicator-list-api'),
]
indicators_api = [
    # API for returning all indicators
    url(
        r'^values/(?P<geometry_identifier>.+)/(?P<geometry_level>.+)/(?P<date>.+)',
        IndicatorsValuesByGeometryDate.as_view(), name='indicators-values-by-geometry-level-date-api'
    ),
]
api = [
    url(r'^geometry/', include(geometry_api)),
    url(r'^indicator/', include(indicator_api)),
    url(r'^indicators/', include(indicators_api)),
    url(
        r'^download-master-data/(?P<date>.+)/check',
        DownloadMasterDataCheck.as_view(),
        name='download-master-data-check'
    ),
    url(
        r'^download-master-data/(?P<date>.+)',
        DownloadMasterData.as_view(),
        name='download-master-data'
    ),
]

instance_url = [
    url(r'^api/', include(api)),
    url(r'^', include('rir_harvester.urls')),
    url(r'^', include('rir_dashboard.urls')),
]

urlpatterns = [
    url(r'^(?P<slug>[^/]+)/', include(instance_url)),
    url(r'^', InstancesView.as_view(), name='instances-view'),
]
