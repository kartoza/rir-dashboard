from datetime import date
from rir_dashboard.views.dashboard._base import BaseDashboardView
from rir_data.serializer.scenario import ScenarioLevelSerializer


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
            self.instance.scenario_levels, many=True
        ).data

        indicators, overall_scenario_level = self.instance.get_indicators_and_overall_scenario

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
