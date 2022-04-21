from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, reverse, redirect
from rir_dashboard.views.dashboard.admin._base import AdminView
from rir_data.models import Indicator, Instance
from rir_harvester.models import Harvester, ExcelHarvester, UsingExposedAPI
from rir_harvester.tasks import run_harvester


class HarvesterIndicatorDetail(AdminView):
    template_name = 'dashboard/admin/harvesters/detail/harvester_detail.html'
    indicator = None

    @property
    def dashboard_title(self):
        return f'Harvester for {self.indicator.full_name}'

    def get_context(self, harvester, edit_url):
        context = {
            'edit_url': edit_url,
            'instance': self.instance,
            'harvester': harvester,
            'harvester_attributes': harvester.get_attributes(),
            'current_log': harvester.harvesterlog_set.first(),
            'can_harvest_now': True
        }
        if harvester.harvester_class in [
            ExcelHarvester[0],
            UsingExposedAPI[0]

        ]:
            context['can_harvest_now'] = False
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
                'meta-ingestor-uuid-view', args=[self.instance.slug, self.kwargs.get('uuid', '')]
            )
        )

    def post(self, request, slug, uuid):
        """
        POST to force harvester to harvest
        """
        instance = get_object_or_404(
            Instance, slug=slug
        )

        try:
            harvester = Harvester.objects.get(unique_id=self.kwargs.get('uuid', ''))
        except Indicator.DoesNotExist:
            raise Http404('Harvester does not exist')
        if harvester.harvester_class in [
            ExcelHarvester[0],
            UsingExposedAPI[0]

        ]:
            return HttpResponseBadRequest('Harvester can not be harvested')
        try:
            run_harvester(harvester.pk)
            return redirect(
                reverse(
                    'harvester-detail', args=[instance.slug, str(harvester.unique_id)]
                )
            )
        except Harvester.DoesNotExist:
            raise Http404('harvester does not exist')
