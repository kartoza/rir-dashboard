import datetime
import json
from django.http import Http404
from django.shortcuts import reverse
from rir_dashboard.views.dashboard.admin._base import AdminView
from rir_data.models import Indicator
from rir_data.serializer.geometry import GeometryContextSerializer


class IndicatorReportingUnitView(AdminView):
    template_name = 'dashboard/admin/indicator/reporting-unit.html'
    indicator = None

    @property
    def dashboard_title(self):
        return f'<span>Indicator Reporting Units</span> : {self.indicator.name} '

    @property
    def context_view(self) -> dict:
        """
        Return context for specific view by instance
        """
        try:
            self.indicator = self.instance.indicators.get(
                id=self.kwargs.get('pk', '')
            )

            context = {
                'indicator': self.indicator,
                'geometries': self.instance.geometries().filter(
                    geometry_level=self.indicator.geometry_reporting_level
                ).order_by('name'),
                'geometry_reporting_units': list(
                    self.indicator.reporting_units.values_list('id', flat=True)
                ),
                'url': reverse(
                    'indicator-reporting-units-api', args=[
                        self.instance.slug, self.indicator.pk
                    ]
                )
            }
            return context
        except Indicator.DoesNotExist:
            raise Http404('Indicator does not found')
