from rest_framework.response import Response
from rest_framework.views import APIView
from scenario.serializer.indicator import IndicatorSerializer
from scenario.serializer.scenario import ScenarioLevelSerializer
from scenario.models.indicator import Indicator
from scenario.models.scenario import ScenarioLevel
from scenario.utils import overall_scenario


class IndicatorsList(APIView):
    """
    Return Indicator List With it's Scenario
    """

    def get(self, request):
        return Response(
            IndicatorSerializer(
                Indicator.list(), many=True
            ).data
        )


class ScenarioList(APIView):
    """
    Return Scenario
    """

    def get(self, request):
        return Response(
            {
                'scenarios': ScenarioLevelSerializer(
                    ScenarioLevel.objects.all(), many=True
                ).data,
                'overall_scenario': ScenarioLevelSerializer(
                    overall_scenario()
                ).data
            }
        )
