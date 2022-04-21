import json
from datetime import datetime
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions import AdminAuthenticationPermission
from rir_data.authentication import IndicatorHarvesterTokenAndBearerAuthentication
from rir_data.models.instance import Instance
from rir_data.models.indicator import Indicator, IndicatorValue, IndicatorValueRejectedError
from rir_data.models.geometry import Geometry, GeometryLevelName, GeometryLevelInstance
from rir_data.serializer.indicator import IndicatorValueSerializer, IndicatorDetailValueSerializer


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
        try:
            value = float(request.POST['value'])
            indicator.save_value(request.POST['date'], geometry, value)
            return Response('OK')
        except ValueError:
            return HttpResponseBadRequest('Value is not a number')
        except IndicatorValueRejectedError as e:
            return HttpResponseBadRequest(f'{e}')


class IndicatorValuesByDate(APIView):
    """
    Return Scenario value for the specific geometry
    Geometry level is the level that the value needs to get
    Return as list of value
    """

    def values(self, slug, pk, geometry_identifier, geometry_level, date,
               use_exact_date=False, more_information=True):
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
        indicator = get_object_or_404(
            instance.indicators, id=pk
        )
        geometry = instance.geometries().get(identifier__iexact=geometry_identifier)
        geometry_level = GeometryLevelName.objects.get(name__iexact=geometry_level)
        date = datetime.strptime(date, "%Y-%m-%d").date()
        return indicator.values(
            geometry, geometry_level, date,
            use_exact_date=use_exact_date, more_information=more_information
        )

    def get(self, request, slug, pk, geometry_identifier, geometry_level, date):
        try:
            return Response(
                self.values(
                    slug, pk, geometry_identifier, geometry_level, date,
                    use_exact_date=False, more_information=True
                )
            )
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


class IndicatorValuesByGeometryAndLevel(APIView):
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
        indicator = get_object_or_404(
            instance.indicators, id=pk
        )
        geometry = instance.geometries().get(identifier__iexact=geometry_identifier)
        geometry_level = GeometryLevelName.objects.get(name__iexact=geometry_level)
        dates = indicator.indicatorvalue_set.values_list(
            'date', flat=True).order_by('date').distinct()

        values = []
        dates_found = []
        for date in dates:
            for value in indicator.values(
                    geometry, geometry_level, date, self.request.GET.get('exact_date', False), more_information=True
            ):
                if 'date' not in value:
                    value['date'] = datetime.today().strftime("%Y-%m-%d")

                if value['date'] not in dates_found:
                    values.append(value)
                    dates_found.append(value['date'])
        return values

    def get(self, request, slug, pk, geometry_identifier, geometry_level):
        try:
            return Response(self.values(slug, pk, geometry_identifier, geometry_level))
        except GeometryLevelName.DoesNotExist:
            raise Http404('The geometry level is not recognized')
        except ValueError:
            return HttpResponseBadRequest('Date format is not correct')


class IndicatorValues(APIView):
    """
    Return Scenario value for country with the indicator geometry level
    """
    authentication_classes = (IndicatorHarvesterTokenAndBearerAuthentication,)

    def get(self, request, slug, pk):
        try:
            instance = get_object_or_404(
                Instance, slug=slug
            )
            indicator = instance.indicators.get(id=pk)
            geometry = instance.geometries().first()
            if geometry:
                try:
                    date = datetime.strptime(
                        request.GET.get('date'), "%Y-%m-%d").date() if request.GET.get('date', None) else datetime.today()
                except ValueError:
                    return HttpResponseBadRequest('Date format should be YYYY-MM-DD')

                return Response(
                    indicator.values(
                        geometry, indicator.geometry_reporting_level, date,
                        serializer=IndicatorDetailValueSerializer
                    )
                )
            else:
                raise Http404('No geometry for the instance')
        except GeometryLevelName.DoesNotExist:
            raise Http404('The geometry level is not recognized')
        except Indicator.DoesNotExist:
            raise Http404('The indicator does not exist')
        except GeometryLevelInstance.DoesNotExist:
            raise Http404('The reporting level is not level of instance')

    def post(self, request, slug, pk):
        """
        Save value for specific date

        :param slug: slug of the instance
        :param pk: pk of the indicator
        :return:
        """
        try:
            instance = get_object_or_404(
                Instance, slug=slug
            )
            data = request.data
            indicator = instance.indicators.get(id=pk)
            geometry = instance.geometries().get(
                identifier__iexact=data['geometry_code']
            )
            if geometry.geometry_level != indicator.geometry_reporting_level:
                return HttpResponseBadRequest(f'Indicator just receives geometry in {indicator.geometry_reporting_level.name} level')

            # Validate the data
            try:
                date = datetime.strptime(
                    data['date'], "%Y-%m-%d").date()
            except ValueError:
                return HttpResponseBadRequest('Date format should be YYYY-MM-DD')
            try:
                value = float(data['value'])
            except ValueError:
                return HttpResponseBadRequest('Value need to be number')

            # extra data needs to be dictionary
            extra_data = data.get('extra_data', None)
            if extra_data:
                try:
                    extra_data.keys()
                except AttributeError:
                    return HttpResponseBadRequest('The extra_data needs to be json')

            # Check if value already exist
            try:
                indicator.indicatorvalue_set.get(
                    date=date,
                    geometry=geometry
                )
                return HttpResponseBadRequest('The value on this date already exist')
            except IndicatorValue.DoesNotExist:
                pass
            indicator_value = indicator.save_value(
                date, geometry, value, extra_data, data.get('details', None)
            )
            return Response(
                IndicatorDetailValueSerializer(indicator_value).data
            )
        except Indicator.DoesNotExist:
            return HttpResponseBadRequest('Indicator does not exist')
        except Geometry.DoesNotExist:
            return HttpResponseBadRequest('Geometry does not exist')
        except KeyError as e:
            return HttpResponseBadRequest(f'{e} is required')
        except IndicatorValueRejectedError as e:
            return HttpResponseBadRequest(f'{e}')


class IndicatorValuesBatch(APIView):
    """
    Return Scenario value for country with the indicator geometry level
    """
    authentication_classes = (IndicatorHarvesterTokenAndBearerAuthentication,)

    def post(self, request, slug, pk):
        """
        Save value for specific date

        :param slug: slug of the instance
        :param pk: pk of the indicator
        :return:
        """
        try:
            instance = get_object_or_404(
                Instance, slug=slug
            )
            rows = request.data
            indicator = instance.indicators.get(id=pk)

            replace = False
            if 'replace' in request.query_params:
                replace = eval(request.query_params['replace'])

            if replace:
                indicator.indicatorvalue_set.all().delete()

            indicator_values = []
            for data in rows:
                geometry = instance.geometries().get(
                    identifier__iexact=data['geometry_code']
                )
                if geometry.geometry_level != indicator.geometry_reporting_level:
                    continue

                # Validate the data
                try:
                    date = datetime.strptime(
                        data['date'], "%Y-%m-%d").date()
                except ValueError:
                    return HttpResponseBadRequest('Date format should be YYYY-MM-DD')
                try:
                    value = float(data['value'])
                except ValueError:
                    return HttpResponseBadRequest('Value need to be number')

                # extra data needs to be dictionary
                extra_data = data.get('extra_data', None)
                if extra_data:
                    try:
                        extra_data.keys()
                    except AttributeError:
                        return HttpResponseBadRequest('The extra_data needs to be json')

                # Check if value already exist
                try:
                    indicator.indicatorvalue_set.get(
                        date=date,
                        geometry=geometry
                    )
                    return HttpResponseBadRequest('The value on this date already exist')
                except IndicatorValue.DoesNotExist:
                    pass
                indicator_values.append(
                    indicator.save_value(
                        date, geometry, value, extra_data, data.get('details', None))
                )
            return Response(
                IndicatorDetailValueSerializer(indicator_values, many=True).data
            )
        except Indicator.DoesNotExist:
            return HttpResponseBadRequest('Indicator does not exist')
        except Geometry.DoesNotExist:
            return HttpResponseBadRequest('Geometry does not exist')
        except KeyError as e:
            return HttpResponseBadRequest(f'{e} is required')
        except IndicatorValueRejectedError as e:
            return HttpResponseBadRequest(f'{e}')
        except NameError:
            return HttpResponseBadRequest(f'replace needs to be True or False')


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
