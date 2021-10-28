from rir_dashboard.views.dashboard._base import BaseDashboardView


class IndicatorView(BaseDashboardView):
    template_name = 'dashboard/indicator.html'

    @property
    def dashboard_title(self):
        return 'Indicator'
