from django.shortcuts import get_object_or_404, redirect, reverse
from rir_dashboard.views.dashboard.admin._base import AdminView
from rir_data.models.indicator import Indicator
from rir_data.models.instance import Instance


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
        context = {
            'indicators': Indicator.objects.filter(group__instance=self.instance)
        }
        return context

    def post(self, request, **kwargs):
        self.instance = get_object_or_404(
            Instance, slug=kwargs.get('slug', '')
        )
        orders = request.POST.get('orders', None)
        if orders:
            orders = orders.split(',')
            for idx, id in enumerate(orders):
                try:
                    indicator = self.instance.indicators.get(id=id)
                    indicator.order = idx
                    indicator.save()
                except Indicator.DoesNotExist:
                    pass
        return redirect(
            reverse(
                'indicator-management-view', args=[self.instance.slug]
            )
        )
