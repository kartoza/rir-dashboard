import json
from datetime import date
from django.shortcuts import reverse
from rir_dashboard.views.dashboard._base import BaseDashboardView
from rir_data.serializer.scenario import ScenarioLevelSerializer
from rir_data.serializer.basemap_layer import BasemapLayerSerializer
from rir_data.serializer.context_layer import ContextLayerSerializer


class ContextAnalysisView(BaseDashboardView):
    template_name = 'dashboard/context-analysis/main.html'

    @property
    def dashboard_title(self):
        return 'Dashboard'

    @property
    def context_view(self) -> dict:
        """
        Return context for specific view by instance
        """
        context = {
            'instance_levels': self.instance.geometry_levels_in_order,
            'url': reverse(
                'geometry-geojson-api', args=[
                    self.instance.slug, 'level', 'date'
                ]
            )
        }

        context['scenarios'] = ScenarioLevelSerializer(
            self.instance.scenario_levels, many=True
        ).data

        context['indicators_in_groups'] = self.instance.get_indicators(self.request.user)
        context['today_date'] = date.today().strftime('%Y-%m-%d')
        context['context_layers'] = json.loads(
            json.dumps(ContextLayerSerializer(self.instance.context_layers, many=True).data)
        )
        context['basemap_layers'] = json.loads(
            json.dumps(BasemapLayerSerializer(self.instance.basemap_layers, many=True).data)
        )
        return context
