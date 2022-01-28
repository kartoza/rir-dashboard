from datetime import date
from django.db.models import Q
from core.models.general import IconTerm, SlugTerm


class Instance(SlugTerm, IconTerm):
    """
    Instance model
    """

    class Meta:
        ordering = ('name',)

    @property
    def scenario_levels(self):
        """
        Return scenarios of the instance
        """
        return self.scenariolevel_set.all()

    @property
    def indicators(self):
        """
        Return indicators of the instance
        """
        from rir_data.models.indicator.indicator import Indicator
        return Indicator.objects.filter(group__instance=self)

    @property
    def geometry_levels(self):
        """
        Return geometry levels of the instance
        """
        from rir_data.models import GeometryLevelName
        return GeometryLevelName.objects.filter(
            pk__in=list(
                self.geometrylevelinstance_set.values_list('level', flat=True)
            )
        )

    @property
    def geometry_instance_levels(self):
        """
        Return geometry levels of the instance
        """
        return self.geometrylevelinstance_set.all()

    @property
    def geometry_levels_in_order(self):
        """
        Return geometry levels of the instance
        """
        levels = []
        levels += self._get_geometry_level_child(
            self.geometry_instance_levels.filter(parent=None)
        )
        return levels

    def _get_geometry_level_child(self, instance_levels):
        levels = []
        for instance_level in instance_levels:
            levels.append(instance_level.level)
            levels += self._get_geometry_level_child(
                self.geometry_instance_levels.filter(parent=instance_level.level)
            )
        return levels

    @property
    def geometry_levels_in_tree(self):
        """
        Return geometry levels of the instance
        """
        from rir_data.utils import get_level_instance_in_tree
        return get_level_instance_in_tree(
            self,
            self.geometry_instance_levels.filter(parent=None)
        )

    @property
    def programs_instance(self):
        """
        Return program of the instance
        """
        return self.programinstance_set.all()

    def geometries(self, date: date = date.today()):
        """
        Return geometries of the instance
        """
        from rir_data.models.geometry import Geometry
        return Geometry.objects.by_date(date).filter(instance=self)

    @property
    def get_indicators_and_overall_scenario(self):
        """
        Return all indicators and overall scenario of the instance
        """
        from rir_data.models.geometry import Geometry, GeometryLevelName
        from rir_data.serializer.indicator import IndicatorSerializer

        indicators = []
        scenario_values = {}
        indicators_in_group = {}
        try:
            country_level = self.geometry_instance_levels.filter(parent=None).first()
            if not country_level:
                raise GeometryLevelName.DoesNotExist

            country_level = country_level.level
            geometry_country = self.geometries().filter(geometry_level=country_level).first()
            if not geometry_country:
                raise Geometry.DoesNotExist

            for indicator in self.indicators:
                values = indicator.values(
                    geometry_country,
                    country_level,
                    date.today()
                )
                data = IndicatorSerializer(indicator).data
                scenario_value = None
                for value in values:
                    scenario_value = value['scenario_value']
                    data['value'] = int(value['value'])
                    data['scenario_value'] = value['scenario_value']
                    data['object'] = indicator
                    data['latest_date'] = indicator.indicatorvalue_set.order_by('date').first().date.strftime("%Y-%m-%d")

                indicators.append(data)

                group_name = indicator.group.name
                if group_name not in indicators_in_group:
                    indicators_in_group[group_name] = {
                        'indicators': [],
                        'indicator_ids': [],
                        'overall_scenario': 1,
                        'overall_scenario_raw': {},
                        'dashboard_link': indicator.group.dashboard_link
                    }
                indicators_in_group[group_name]['indicators'].append(data)
                indicators_in_group[group_name]['indicator_ids'].append(str(indicator.id))

                # create overall scenarios
                if indicator.show_in_context_analysis and scenario_value:
                    if scenario_value not in scenario_values:
                        scenario_values[scenario_value] = 0
                    scenario_values[scenario_value] += 1

                    # this is for the group
                    if scenario_value not in indicators_in_group[group_name]['overall_scenario_raw']:
                        indicators_in_group[group_name]['overall_scenario_raw'][scenario_value] = 0
                    indicators_in_group[group_name]['overall_scenario_raw'][scenario_value] += 1
        except (Geometry.DoesNotExist, GeometryLevelName.DoesNotExist):
            pass

        # get the overall scenario
        sorted_scenario_values = {key: scenario_values[key] for key in sorted(scenario_values.keys())}
        try:
            overall_scenario_level = max(sorted_scenario_values, key=sorted_scenario_values.get)
        except ValueError:
            overall_scenario_level = 1

        # overall scenario for each of group
        for group_name, group in indicators_in_group.items():
            sorted_scenario_values = {key: group['overall_scenario_raw'][key] for key in sorted(group['overall_scenario_raw'].keys())}
            try:
                overall_scenario_level = max(sorted_scenario_values, key=sorted_scenario_values.get)
            except ValueError:
                overall_scenario_level = 1
            group['overall_scenario'] = overall_scenario_level
            group['indicator_ids'] = ','.join(group['indicator_ids'])

        return indicators_in_group, overall_scenario_level

    @property
    def context_layers(self):
        """
        Return context layers of the instance
        """
        from rir_data.models import ContextLayer
        return ContextLayer.objects.filter(Q(instance__isnull=True) | Q(instance=self)).filter(show_on_map=True)

    @property
    def basemap_layers(self):
        """
        Return basemap layers of the instance
        """
        from rir_data.models import BasemapLayer
        return BasemapLayer.objects.filter(Q(instance__isnull=True) | Q(instance=self)).filter(show_on_map=True)

    @property
    def links(self):
        """
        Return links of the instance
        """
        from rir_data.models import Link
        return Link.objects.filter(Q(instance__isnull=True) | Q(instance=self))
