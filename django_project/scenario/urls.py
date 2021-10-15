__author__ = 'Irwan Fathurrahman <meomancer@gmail.com>'
__date__ = '19/08/20'

from django.conf.urls import url
from scenario.api.program import ProgramList, ProgramDetail
from scenario.api.scenario import IndicatorsList, ScenarioList

urlpatterns = [
    url(r'^list', ScenarioList.as_view(), name='scenario_list'),
    url(r'^indicator', IndicatorsList.as_view(), name='indicator_list'),
    url(r'^program/(?P<program_name>.+)', ProgramDetail.as_view(), name='program_detail'),
    url(r'^program', ProgramList.as_view(), name='program_list'),
]
