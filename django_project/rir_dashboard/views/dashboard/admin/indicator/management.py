import json
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, reverse
from rir_dashboard.views.dashboard.admin._base import AdminView
from rir_data.models.indicator import Indicator, IndicatorGroup
from rir_data.models.instance import Instance
from rir_harvester.models.harvester import UsingExposedAPI


class IndicatorManagementView(AdminView):
    template_name = 'dashboard/admin/indicator/management.html'

    @property
    def dashboard_title(self):
        return 'Indicator Management'

    @property
    def context_view(self) -> dict:
        """
        Return context for specific view by instance
        """
        indicators_in_groups = self.instance.get_indicators(self.request.user)
        for excluded_group in self.instance.indicatorgroup_set.exclude(
                name__in=indicators_in_groups.keys()):
            indicators_in_groups[excluded_group.name] = {
                'indicators': []
            }

        context = {
            'indicators_in_groups': indicators_in_groups,
            'external_exposed_api': UsingExposedAPI[0]
        }
        return context

    def post(self, request, **kwargs):
        self.instance = get_object_or_404(
            Instance, slug=kwargs.get('slug', '')
        )
        orders = request.POST.get('orders', None)
        if not orders:
            return HttpResponseBadRequest(f'Orders is required')

        orders = json.loads(orders)
        indicators = self.instance.indicators
        groups = self.instance.indicatorgroup_set.all()
        idx = 1
        for group_name, ids in orders.items():
            try:
                group = groups.get(name=group_name)
                for id in ids:
                    try:
                        indicator = indicators.get(id=id)
                        indicator.group = group
                        indicator.order = idx
                        idx += 1
                        indicator.save()
                    except Indicator.DoesNotExist:
                        pass
            except IndicatorGroup.DoesNotExist:
                pass
        return redirect(
            reverse(
                'indicator-management-view', args=[self.instance.slug]
            )
        )
