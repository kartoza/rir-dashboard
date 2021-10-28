from rir_dashboard.views.dashboard._base import BaseDashboardView


class DashboardHomeView(BaseDashboardView):
    template_name = 'dashboard/home.html'

    @property
    def dashboard_title(self):
        return 'Dashboard'
