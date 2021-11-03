import json
from datetime import datetime
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rir_data.serializer.indicator import IndicatorSerializer
from rir_data.models.instance import Instance
from rir_data.models.geometry import Geometry, GeometryLevelName


class IndicatorsList(APIView):
    """
    Return Indicator List With it's Scenario
    """

    def get(self, request, slug):
        instance = get_object_or_404(
            Instance, slug=slug
        )
        return Response(
            IndicatorSerializer(
                instance.indicators, many=True
            ).data
        )


class IndicatorValues(APIView):
    """
    Return Scenario value for the specific geometry
    Geometry level is the level that the value needs to get
    Return as geojson of geometry
    """

    def values(self, slug, pk, geometry_identifier, geometry_level, date):
        """
        Return values of the indicator

        :param pk: pk of the indicator
        :param geometry_identifier: the geometry identifier
        :param geometry_level: the geometry level that will be checked
        :param date: the date of data
        :return:
        """
        instance = get_object_or_404(
            Instance, slug=slug
        )
        indicator = instance.indicators.get(id=pk)
        geometry = instance.geometries().get(identifier__iexact=geometry_identifier)
        geometry_level = GeometryLevelName.objects.get(name__iexact=geometry_level)
        date = datetime.strptime(date, "%Y-%m-%d").date()
        return indicator.values(geometry, geometry_level, date)

    def get(self, request, slug, pk, geometry_identifier, geometry_level, date):
        try:
            return Response(self.values(slug, pk, geometry_identifier, geometry_level, date))
        except GeometryLevelName.DoesNotExist:
            raise Http404('The geometry level is not recognized')
        except ValueError:
            return HttpResponseBadRequest('Date format is not correct')


class IndicatorValuesGeojson(IndicatorValues):
    """
    Return geojson Scenario value for the specific geometry
    Geometry level is the level that the value needs to get
    Return as geojson of geometry
    """

    def get(self, request, slug, pk, geometry_identifier, geometry_level, date):
        try:
            values = self.values(slug, pk, geometry_identifier, geometry_level, date)
            features = []
            for value in values:
                try:
                    geometry = Geometry.objects.get(id=value['geometry_id'])
                    features.append(
                        {
                            "type": "Feature",
                            "properties": value,
                            "geometry": json.loads(
                                geometry.geometry.geojson
                            )
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

        except GeometryLevelName.DoesNotExist:
            return HttpResponseBadRequest('The geometry level is not recognized')
        except ValueError:
            return HttpResponseBadRequest('Date format is not correct')
