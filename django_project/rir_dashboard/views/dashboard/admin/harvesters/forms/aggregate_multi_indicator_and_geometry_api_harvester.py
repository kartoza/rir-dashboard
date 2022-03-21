from rir_dashboard.views.dashboard.admin.harvesters.forms._base import HarvesterFormView
from rir_harvester.harveters.aggregate_multi_indicator_and_geometry_api_harvester import AggregateMultiIndicatorAndGeometryAPIHarvester
from rir_harvester.models.harvester import Harvester, EtoolsProgramCoverageHarvesterTuple
from rir_harvester.models.harvester_attribute import HarvesterAttribute
from rir_harvester.tasks import run_harvester


# This harvester is just 1 for each instance
class AggregaretMultiIndicatorAndGeometryAPIHarvesterView(HarvesterFormView):
    harvester_class = AggregateMultiIndicatorAndGeometryAPIHarvester
    template_name = 'dashboard/admin/harvesters/forms/etools/program-coverage.html'

    @property
    def dashboard_title(self):
        return f'Aggregate Multi Indicator and Geometry AP IHarvester'

    def get_indicator(self):
        """
         Return indicator and save it as attribute
        """
        return None

    def get_harvester(self) -> Harvester:
        """
         Return harvester
        """
        attribute = HarvesterAttribute.objects.filter(
            name='instance_slug',
            value=self.instance.slug,
            harvester__indicator=None,
            harvester__harvester_class=EtoolsProgramCoverageHarvesterTuple[0]
        ).first()
        if attribute:
            return attribute.harvester
        raise Harvester.DoesNotExist()

    @property
    def harvesters(self) -> tuple:
        """
         Return harvesters
        """
        return (
            EtoolsProgramCoverageHarvesterTuple,
        )

    @property
    def context_view(self) -> dict:
        """
        Return context for specific view by instance
        """
        context = super().context_view
        context['indicators'] = []
        for indicator in self.instance.indicators.order_by('group__name', 'name'):
            context['indicators'].append(indicator.group.name + '/' + indicator.name)
        for attr in context['attributes']:
            if attr['name'] == 'instance_slug':
                attr['value'] = self.instance.slug
        return context

    def after_post(self, harvester: Harvester):
        """
         Called after post success
        """
        run_harvester.delay(harvester.pk)
