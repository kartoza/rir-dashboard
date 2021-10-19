import json
from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from core.models import Geometry, GeometryLevel
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


class IndicatorValues(APIView):
    """
    Return Scenario value for the specific geometry
    Geometry level is the level that the value needs to get
    Return as geojson of geometry
    """

    def values(self, id, geometry_identifier, geometry_level, date):
        indicator = get_object_or_404(Indicator, id=id)
        geometry = get_object_or_404(Geometry, identifier__iexact=geometry_identifier)
        geometry_level = GeometryLevel.objects.get(name__iexact=geometry_level)
        date = datetime.strptime(date, "%Y-%m-%d").date()
        return indicator.values(geometry, geometry_level, date)

    def get(self, request, id, geometry_identifier, geometry_level, date):
        try:
            return Response(self.values(id, geometry_identifier, geometry_level, date))

        except GeometryLevel.DoesNotExist:
            return HttpResponseBadRequest('The geometry level is not recognized')
        except ValueError:
            return HttpResponseBadRequest('Date format is not correct')


class IndicatorValuesGeojson(IndicatorValues):
    """
    Return geojson Scenario value for the specific geometry
    Geometry level is the level that the value needs to get
    Return as geojson of geometry
    """

    def get(self, request, id, geometry_identifier, geometry_level, date):
        try:
            values = self.values(id, geometry_identifier, geometry_level, date)
            features = []
            for value in values:
                try:
                    geometry = Geometry.objects.get(id=value['geometry_id'])
                    features.append(
                        {
                            "type": "Feature",
                            "properties": value,
                            "geometry": json.loads(
                                geometry.geometry.geojson)
                        }
                    )
                except Geometry.DoesNotExist:
                    pass
            return Response(
                {
                    "type": "FeatureCollection",
                    "features": features
                }
            )

        except GeometryLevel.DoesNotExist:
            return HttpResponseBadRequest('The geometry level is not recognized')
        except ValueError:
            return HttpResponseBadRequest('Date format is not correct')
