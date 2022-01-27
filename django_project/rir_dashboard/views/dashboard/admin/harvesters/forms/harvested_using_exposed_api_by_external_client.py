from rir_harvester.harveters.using_exposed_api import UsingExposedAPI
from ._base import HarvesterFormView


class HarvestedUsingExposedAPIByExternalClientView(HarvesterFormView):
    harvester_class = UsingExposedAPI
    template_name = 'dashboard/admin/harvesters/forms/_base_attribute.html'

    @property
    def context_view(self) -> dict:
        """
        Return context for specific view by instance
        """
        context = super().context_view
        context['reporting_units'] = self.indicator.reporting_units.order_by('name')
        return context
