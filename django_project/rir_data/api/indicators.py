from datetime import datetime
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from rir_data.models.instance import Instance
from rir_data.models.geometry import Geometry, GeometryLevelName
from rir_data.models.scenario import ScenarioLevel
from rir_data.serializer.indicator import IndicatorSerializer


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


class IndicatorsGroupValuesByGeometryDate(APIView):
    """
    Return values of all indicators by date and and geometry
    """

    def get(self, request, slug, geometry_identifier, geometry_level, date):
        try:

            instance = get_object_or_404(
                Instance, slug=slug
            )
            geometry = instance.geometries().get(identifier__iexact=geometry_identifier)
            geometry_level = GeometryLevelName.objects.get(name__iexact=geometry_level)
            date = datetime.strptime(date, "%Y-%m-%d").date()
            indicators_in_group = {}
            for indicator in instance.indicators:
                values = indicator.values(
                    geometry, geometry_level, date
                )

                group_name = indicator.group.name
                if group_name not in indicators_in_group:
                    indicators_in_group[group_name] = {
                        'values': [],
                        'indicators': [],
                        'overall_scenario': 0,
                        'overall_scenario_text': '',
                        'overall_scenario_color': ''
                    }

                for value in values:
                    value['indicator_id'] = indicator.id
                    indicators_in_group[group_name]['indicators'].append(value)
                    indicators_in_group[group_name]['values'].append(value['scenario_value'])

            # overall scenario for each of group
            for group_name, group in indicators_in_group.items():
                try:
                    overall_scenario_level = max(set(group['values']), key=group['values'].count)
                except ValueError:
                    overall_scenario_level = 0
                group['overall_scenario'] = overall_scenario_level
                try:
                    scenario_level = ScenarioLevel.objects.get(
                        instance=instance, level=overall_scenario_level)
                    group['overall_scenario_text'] = scenario_level.name
                    group['overall_scenario_color'] = scenario_level.background_color
                except ScenarioLevel.DoesNotExist:
                    pass
                del group['values']
            return Response(indicators_in_group)
        except Geometry.DoesNotExist:
            raise Http404('Geometry does not exist')
        except GeometryLevelName.DoesNotExist:
            raise Http404('Geometry level does not exist')


class IndicatorsValuesByGeometryDate(APIView):
    """
    Return values of all indicators by date and and geometry
    """

    def get(self, request, slug, geometry_identifier, geometry_level, date):
        try:

            instance = get_object_or_404(
                Instance, slug=slug
            )
            geometry = instance.geometries().get(identifier__iexact=geometry_identifier)
            geometry_level = GeometryLevelName.objects.get(name__iexact=geometry_level)
            date = datetime.strptime(date, "%Y-%m-%d").date()
            output = []
            for indicator in instance.indicators:
                values = indicator.values(
                    geometry, geometry_level, date
                )
                for value in values:
                    value['indicator_id'] = indicator.id
                    value['group_name'] = indicator.group.name
                    output.append(value)
            return Response(output)
        except Geometry.DoesNotExist:
            raise Http404('Geometry does not exist')
        except GeometryLevelName.DoesNotExist:
            raise Http404('Geometry level does not exist')
