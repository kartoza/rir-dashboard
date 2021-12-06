from django.http import Http404
from django.shortcuts import get_object_or_404, reverse, redirect
from rir_dashboard.views.dashboard.admin._base import AdminView
from rir_data.models import Indicator, Instance
from rir_harvester.models import Harvester
from rir_harvester.tasks import run_harvester


class HarvesterDetail(AdminView):
    template_name = 'dashboard/admin/harvesters/detail.html'
    indicator = None

    @property
    def dashboard_title(self):
        return f'Harvester for {self.indicator.__str__()}'

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
            raise Http404('Indicator does not found')

        try:
            harvester = self.indicator.harvester
        except Harvester.DoesNotExist:
            raise Http404('Harvester does not found')

        context = {
            'indicator': self.indicator,
            'harvester': harvester
        }
        return context

    def post(self, request, slug, pk):
        instance = get_object_or_404(
            Instance, slug=slug
        )

        try:
            self.indicator = instance.indicators.get(
                id=self.kwargs.get('pk', '')
            )
        except Indicator.DoesNotExist:
            raise Http404('Indicator does not found')
        try:
            harvester = self.indicator.harvester
            run_harvester.delay(harvester.pk)

            return redirect(
                reverse(
                    'harvester-detail', args=[instance.slug, self.indicator.pk]
                )
            )
        except Harvester.DoesNotExist:
            raise Http404('harvester does not found')
