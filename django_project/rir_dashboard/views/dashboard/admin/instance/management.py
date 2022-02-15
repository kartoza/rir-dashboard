from rir_dashboard.views.dashboard.admin._base import AdminView


class InstanceManagementView(AdminView):
    template_name = 'dashboard/admin/instance/management.html'

    @property
    def dashboard_title(self):
        return 'Instance Management'
