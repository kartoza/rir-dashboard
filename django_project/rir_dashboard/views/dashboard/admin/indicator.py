import datetime
import json
from django.http import Http404
from django.shortcuts import reverse
from rir_dashboard.views.dashboard.admin._base import AdminView
from rir_data.models import Indicator
from rir_data.serializer.geometry import GeometryContextSerializer


class IndicatorValueManagerMapView(AdminView):
    template_name = 'dashboard/admin/indicator-value-manager-map.html'
    indicator = None
    scenario_level = None

    @property
    def dashboard_title(self):
        return f'<span>Indicator Value Manager Map</span> : {self.indicator.name} '

    @property
    def context_view(self) -> dict:
        """
        Return context for specific view by instance
        """
        try:
            self.indicator = self.instance.indicators.get(
                id=self.kwargs.get('pk', '')
            )

            legends = {
                'NODATA': {
                    'name': 'No Data',
                    'color': 'gray'
                },
                'LATESTDATAFOUND': {
                    'name': 'Has Data',
                    'color': 'green'
                },
                'NEEDUPDATE': {
                    'name': 'Need Update Data',
                    'color': 'red'
                }
            }
            context = {
                'indicator': self.indicator,
                'geometry': json.loads(
                    json.dumps(
                        GeometryContextSerializer(
                            self.instance.geometries().filter(geometry_level=self.indicator.geometry_reporting_level),
                            many=True).data
                    )
                ),
                'geometry_has_updated_value': list(set(self.indicator.query_value(datetime.date.today()).values_list('geometry', flat=True))),
                'geometry_has_value': list(set(self.indicator.indicatorvalue_set.values_list('geometry', flat=True))),
                'legends': legends,
                'url_value_by_geometry': reverse('indicator-values-by-geometry', args=[
                    self.instance.slug, self.indicator.id, 0
                ])
            }
            return context
        except Indicator.DoesNotExist:
            raise Http404('Indicator does not found')
