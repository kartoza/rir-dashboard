from datetime import datetime
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rir_data.models.instance import Instance
from rir_data.models.geometry import GeometryLevelName
from rir_data.serializer.geometry import GeometrySerializer


class GeometryGeojsonAPI(APIView):
    """
    Return geometry of instance
    """

    def get(self, request, slug, geometry_level, date):
        """
        Return values of the indicator

        :param geometry_level: the geometry level that will be returned
        :param date: the date of data
        :return:
        """
        try:
            instance = get_object_or_404(
                Instance, slug=slug
            )
            date = datetime.strptime(date, "%Y-%m-%d").date()
            geometry_level = GeometryLevelName.objects.get(name__iexact=geometry_level)
            geometries = instance.geometries(date).filter(geometry_level=geometry_level)
            return Response(GeometrySerializer(geometries, many=True).data)
        except GeometryLevelName.DoesNotExist:
            raise Http404('The geometry level is not recognized')
        except ValueError:
            return HttpResponseBadRequest('Date format is not correct')
