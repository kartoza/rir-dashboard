from rest_framework.response import Response
from rest_framework.views import APIView
from rir_data.serializer.scenario import ScenarioLevelSerializer
from rir_data.models.scenario import ScenarioLevel


class ScenarioList(APIView):
    """
    Return Scenario
    """

    def get(self, request):
        return Response(
            ScenarioLevelSerializer(
                ScenarioLevel.objects.all(), many=True
            ).data
        )