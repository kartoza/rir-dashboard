from django.http import Http404
from django.shortcuts import get_object_or_404, reverse, redirect
from rir_dashboard.views.dashboard.admin._base import AdminView
from rir_data.models import Indicator, Instance
from rir_harvester.models import Harvester
from rir_harvester.tasks import run_harvester


class HarvesterIndicatorDetail(AdminView):
    template_name = 'dashboard/admin/harvesters/detail/indicator_detail.html'
    indicator = None

    @property
    def dashboard_title(self):
        return f'Harvester for {self.indicator.__str__()}'

    def get_context(self, harvester, edit_url):
        context = {
            'edit_url': edit_url,
            'instance': self.instance,
            'harvester': harvester,
            'harvester_attributes': harvester.get_attributes(),
            'current_log': harvester.harvesterlog_set.first()
        }
        return context

    @property
    def context_view(self) -> dict:
        """
        Return context for specific view by instance
        """
        try:
            self.indicator = self.instance.indicators.get(
                id=self.kwargs.get('pk', '')
            )
        except Indicator.DoesNotExist:
            raise Http404('Indicator does not exist')

        try:
            harvester = self.indicator.harvester
        except Harvester.DoesNotExist:
            raise Http404('Harvester does not exist')

        return self.get_context(
            harvester, reverse(
                self.indicator.harvester.harvester_class, args=[self.instance.slug, self.indicator.id]
            )
        )

    def post(self, request, slug, pk):
        """
        POST to force harvester to harvest
        """
        instance = get_object_or_404(
            Instance, slug=slug
        )

        try:
            self.indicator = instance.indicators.get(
                id=self.kwargs.get('pk', '')
            )
        except Indicator.DoesNotExist:
            raise Http404('Indicator does not exist')
        try:
            harvester = self.indicator.harvester
            run_harvester.delay(harvester.pk)

            return redirect(
                reverse(
                    'harvester-indicator-detail', args=[instance.slug, self.indicator.pk]
                )
            )
        except Harvester.DoesNotExist:
            raise Http404('harvester does not exist')


class HarvesterDetail(HarvesterIndicatorDetail):
    template_name = 'dashboard/admin/harvesters/detail/harvester_detail.html'
    indicator = None

    @property
    def dashboard_title(self):
        return f'Harvester detail'

    @property
    def context_view(self) -> dict:
        """
        Return context for specific view by instance
        """

        try:
            harvester = Harvester.objects.get(unique_id=self.kwargs.get('uuid', ''))
        except Indicator.DoesNotExist:
            raise Http404('Harvester does not exist')

        return self.get_context(
            harvester, reverse(
                'meta-harvester-uuid-view', args=[self.instance.slug, self.kwargs.get('uuid', '')]
            )
        )
