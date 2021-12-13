import json
from datetime import datetime
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions import AdminAuthenticationPermission
from rir_data.serializer.indicator import IndicatorSerializer
from rir_data.models.instance import Instance
from rir_data.models.indicator import Indicator, IndicatorValue
from rir_data.models.geometry import Geometry, GeometryLevelName
from rir_data.serializer.indicator import IndicatorValueSerializer


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


class IndicatorValuesByGeometry(APIView):
    """
    Return Scenario value for the specific geometry
    for all date
    """
    permission_classes = (IsAuthenticated, AdminAuthenticationPermission,)

    def get(self, request, slug, pk, geometry_pk):
        """
        Return values of the indicator

        :param slug: slug of the instance
        :param pk: pk of the indicator
        :param geometry_pk: the geometry id
        :return:
        """
        instance = get_object_or_404(
            Instance, slug=slug
        )
        geometry = get_object_or_404(
            Geometry, id=geometry_pk
        )
        try:
            indicator = instance.indicators.get(id=pk)
            values = indicator.indicatorvalue_set.filter(geometry=geometry).order_by('-date')
            return Response(IndicatorValueSerializer(values, many=True).data)
        except GeometryLevelName.DoesNotExist:
            raise Http404('The geometry level is not recognized')
        except ValueError:
            return HttpResponseBadRequest('Date format is not correct')

    def post(self, request, slug, pk, geometry_pk):
        """
        Return values of the indicator

        :param slug: slug of the instance
        :param pk: pk of the indicator
        :param geometry_pk: the geometry id
        :return:
        """
        instance = get_object_or_404(
            Instance, slug=slug
        )
        geometry = get_object_or_404(
            Geometry, id=geometry_pk
        )
        indicator = instance.indicators.get(id=pk)
        IndicatorValue.objects.get_or_create(
            indicator=indicator,
            geometry=geometry,
            date=request.POST['date'],
            defaults={
                'value': request.POST['value']
            }
        )
        return Response('OK')


class IndicatorValuesByDate(APIView):
    """
    Return Scenario value for the specific geometry
    Geometry level is the level that the value needs to get
    Return as list of value
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


class IndicatorValuesByDateAndGeojson(IndicatorValuesByDate):
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


class IndicatorValues(APIView):
    """
    Return Scenario value for the specific geometry
    Geometry level is the level that the value needs to get
    """

    def values(self, slug, pk, geometry_identifier, geometry_level):
        """
        Return values of the indicator

        :param pk: pk of the indicator
        :param geometry_identifier: the geometry identifier
        :param geometry_level: the geometry level that will be checked
        :return:
        """
        instance = get_object_or_404(
            Instance, slug=slug
        )
        indicator = instance.indicators.get(id=pk)
        geometry = instance.geometries().get(identifier__iexact=geometry_identifier)
        geometry_level = GeometryLevelName.objects.get(name__iexact=geometry_level)
        dates = indicator.indicatorvalue_set.values_list(
            'date', flat=True).order_by('date').distinct()
        values = []
        for date in dates:
            values += indicator.values(
                geometry, geometry_level, date, True
            )
        return values

    def get(self, request, slug, pk, geometry_identifier, geometry_level):
        try:
            return Response(self.values(slug, pk, geometry_identifier, geometry_level))
        except GeometryLevelName.DoesNotExist:
            raise Http404('The geometry level is not recognized')
        except ValueError:
            return HttpResponseBadRequest('Date format is not correct')


class IndicatorReportingUnits(APIView):
    """
    Change reporting units of indicator
    """
    permission_classes = (IsAuthenticated, AdminAuthenticationPermission,)

    def post(self, request, slug, pk):
        """
        Save reporting units of indicator

        :param slug: slug of the instance
        :param pk: pk of the indicator
        :return:
        """
        try:
            instance = get_object_or_404(
                Instance, slug=slug
            )
            indicator = instance.indicators.get(id=pk)
            indicator.geometry_reporting_units.clear()
            ids = request.POST['ids'].split(',')
            if len(ids) > 0:
                if ids[0]:
                    indicator.geometry_reporting_units.add(*Geometry.objects.filter(id__in=ids))
            return Response('OK')
        except Indicator.DoesNotExist:
            raise Http404('Indicator does not exist')
        except KeyError:
            return HttpResponseBadRequest('ids is needed in data')
