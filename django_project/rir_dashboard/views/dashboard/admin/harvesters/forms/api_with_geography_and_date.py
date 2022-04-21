from rir_harvester.harveters.api_with_geography_and_date import APIWithGeographyAndDate
from ._base import HarvesterFormView


class HarvesterAPIWithGeographyAndDateView(HarvesterFormView):
    harvester_class = APIWithGeographyAndDate
    template_name = 'dashboard/admin/harvesters/forms/api_with_geography.html'

    @property
    def context_view(self) -> dict:
        """
        Return context for specific view by instance
        """
        context = super().context_view
        context['reporting_units'] = self.indicator.reporting_units.order_by('name')
        return context
