from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rir_data.serializer.program import ProgramSerializer
from rir_data.models.program import Program


class ProgramList(APIView):
    """
    Return Program List With it's Interventions
    """

    def get(self, request):
        return Response(
            ProgramSerializer(
                Program.objects.all(), many=True
            ).data
        )


class ProgramDetail(APIView):
    """
    Return Program Detail
    """

    def get(self, request, program_name):
        program = get_object_or_404(Program, name__iexact=program_name)
        return Response(
            ProgramSerializer(program).data
        )
