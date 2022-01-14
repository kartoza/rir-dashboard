from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rir_data.models.instance import Instance
from rir_harvester.models.harvester_log import HarvesterLog
from rir_harvester.serializer.harvester import HarvesterLogSerializer


class HarvesterLogData(APIView):
    """
    Return HarvesterLog data
    """

    def get(self, request, slug, pk):
        get_object_or_404(
            Instance, slug=slug
        )
        log = get_object_or_404(
            HarvesterLog, pk=pk
        )
        return Response(
            HarvesterLogSerializer(log).data
        )
