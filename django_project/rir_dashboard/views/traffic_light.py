from datetime import date
from django.contrib.auth.views import LoginView

from core.models.general import Geometry, GeometryLevel
from rir_data.models.scenario import ScenarioLevel
from rir_data.models.indicator import Indicator
from rir_data.models.program import ProgramIntervention
from rir_data.serializer.scenario import ScenarioLevelSerializer
from rir_data.serializer.indicator import IndicatorSerializer


class TrafficLightView(LoginView):
    template_name = 'pages/traffic_light.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['scenarios'] = ScenarioLevelSerializer(
            ScenarioLevel.objects.all(), many=True
        ).data

        # Somalia
        indicators = []
        scenario_values = {}

        # get indicators
        try:
            for indicator in Indicator.objects.all():
                values = indicator.values(
                    Geometry.objects.get(identifier__iexact='SO'),
                    GeometryLevel.objects.get(name__iexact='country'),
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
        except (Geometry.DoesNotExist, GeometryLevel.DoesNotExist):
            pass

        # get the overall scenario
        interventions = []
        sorted_scenario_values = {key: scenario_values[key] for key in sorted(scenario_values.keys())}
        overall_scenario = 1
        if sorted_scenario_values:
            overall_scenario_level = max(sorted_scenario_values, key=sorted_scenario_values.get)
            overall_scenario = context['scenarios'][overall_scenario_level - 1]

            # intervention
            for intervention in ProgramIntervention.objects.order_by('scenario_level__name').filter(scenario_level__level=overall_scenario_level):
                interventions.append({
                    'program_id': intervention.program.id,
                    'program_name': intervention.program.name,
                    'url': intervention.intervention_url,
                })

        context['overall_scenario'] = overall_scenario
        context['interventions'] = interventions
        context['indicators'] = indicators
        context['today_date'] = date.today().strftime('%Y-%m-%d')
        return context
