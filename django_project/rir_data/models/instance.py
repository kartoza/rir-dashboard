from datetime import date
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
        return self.geometrylevelinstance_set.all()

    @property
    def geometry_levels_in_order(self):
        """
        Return geometry levels of the instance
        """
        top = self.geometry_levels.filter(parent=None).first()
        levels = []
        if top:
            levels = [top.level]
            child = self.geometry_levels.filter(parent=top.level).first()
            while child is not None:
                if child:
                    levels.append(child.level)
                child = self.geometry_levels.filter(parent=child.level).first()

        return levels

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
        try:
            country_level = self.geometry_levels.filter(parent=None).first()
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

                indicators.append(data)

                # create overall scenarios
                if indicator.show_in_context_analysis and scenario_value:
                    if scenario_value not in scenario_values:
                        scenario_values[scenario_value] = 0
                    scenario_values[scenario_value] += 1
        except (Geometry.DoesNotExist, GeometryLevelName.DoesNotExist):
            pass

        # get the overall scenario
        sorted_scenario_values = {key: scenario_values[key] for key in sorted(scenario_values.keys())}
        try:
            overall_scenario_level = max(sorted_scenario_values, key=sorted_scenario_values.get)
        except ValueError:
            overall_scenario_level = 1

        return indicators, overall_scenario_level

    @property
    def context_layers(self):
        """
        Return context layers of the instance
        """
        return self.contextlayer_set.filter(show_on_map=True)
