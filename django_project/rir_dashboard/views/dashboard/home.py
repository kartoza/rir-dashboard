from datetime import date
from rir_dashboard.views.dashboard._base import BaseDashboardView
from rir_data.serializer.scenario import ScenarioLevelSerializer
from rir_data.serializer.indicator import IndicatorSerializer
from rir_data.models.geometry import Geometry, GeometryLevelName


class DashboardHomeView(BaseDashboardView):
    template_name = 'dashboard/home.html'

    @property
    def dashboard_title(self):
        return 'Dashboard'

    @property
    def context_view(self) -> dict:
        """
        Return context for specific view by instance
        """
        context = {}
        context['scenarios'] = ScenarioLevelSerializer(
            self.instance.scenarios, many=True
        ).data

        # Somalia
        indicators = []
        scenario_values = {}

        # TODO : Fix this using Instance Geometry Level
        try:
            country_level = self.instance.geometry_levels.filter(parent=None).first()
            if country_level:
                country_level = country_level.level
                geometry_country = self.instance.geometries.filter(geometry_level=country_level).first()

                for group in self.instance.indicator_groups:
                    for indicator in group.indicator_set.all():
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
                        if indicator.show_in_traffic_light and scenario_value:
                            if scenario_value not in scenario_values:
                                scenario_values[scenario_value] = 0
                            scenario_values[scenario_value] += 1
        except (Geometry.DoesNotExist, GeometryLevelName.DoesNotExist):
            pass

        # get the overall scenario
        sorted_scenario_values = {key: scenario_values[key] for key in sorted(scenario_values.keys())}
        overall_scenario_level = max(sorted_scenario_values, key=sorted_scenario_values.get)

        # intervention
        interventions = []
        for program in self.instance.programs:
            intervention = program.programintervention_set.filter(scenario_level__level=overall_scenario_level).first()
            if intervention:
                interventions.append({
                    'program_id': intervention.program.id,
                    'program_name': intervention.program.name,
                    'url': intervention.intervention_url,
                })
        context['overall_scenario'] = context['scenarios'][overall_scenario_level - 1]
        context['indicators'] = indicators
        context['interventions'] = interventions
        context['today_date'] = date.today().strftime('%Y-%m-%d')
        return context
