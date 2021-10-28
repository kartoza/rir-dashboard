from rest_framework.response import Response
from rest_framework.views import APIView
from rir_data.serializer.indicator import IndicatorSerializer
from rir_data.models.indicator import Indicator


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
