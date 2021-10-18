from django.conf.urls import url
from rir_data.api.program import ProgramList, ProgramDetail
from rir_data.api.scenario import ScenarioList
from rir_data.api.indicator import IndicatorsList

urlpatterns = [
    url(r'^scenarios/values', ScenarioList.as_view(), name='scenario_list'),
    url(r'^scenarios', ScenarioList.as_view(), name='scenario_list'),
    url(r'^indicators', IndicatorsList.as_view(), name='indicator_list'),
    url(r'^programs/(?P<program_name>.+)', ProgramDetail.as_view(), name='program_detail'),
    url(r'^programs', ProgramList.as_view(), name='program_list'),
]
