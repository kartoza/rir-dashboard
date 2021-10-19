from django.conf.urls import url
from django.urls import include
from rir_data.api.program import ProgramList, ProgramDetail
from rir_data.api.scenario import ScenarioList
from rir_data.api.indicator import (
    IndicatorsList, IndicatorValues, IndicatorValuesGeojson
)

indicators_url = [
    url(
        r'^(?P<id>\d+)/values/(?P<geometry_identifier>.+)/(?P<geometry_level>.+)/(?P<date>.+).geojson',
        IndicatorValuesGeojson.as_view(), name='indicator_values_geojson'),
    url(
        r'^(?P<id>\d+)/values/(?P<geometry_identifier>.+)/(?P<geometry_level>.+)/(?P<date>.+)',
        IndicatorValues.as_view(), name='indicator_values'),
    url(r'^', IndicatorsList.as_view(), name='indicator_list'),
]

urlpatterns = [
    url(r'^indicators/', include(indicators_url)),
    url(r'^scenarios', ScenarioList.as_view(), name='scenario_list'),
    url(r'^programs/(?P<program_name>.+)', ProgramDetail.as_view(), name='program_detail'),
    url(r'^programs', ProgramList.as_view(), name='program_list'),
]
