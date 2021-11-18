from rir_dashboard.views.dashboard.admin._base import AdminView
from rir_data.models.instance import Instance


class InstanceManagementView(AdminView):
    template_name = 'dashboard/admin/instance/management.html'

    @property
    def dashboard_title(self):
        return 'Instance Management'

    @property
    def context_view(self) -> dict:
        """
        Return context for specific view by instance
        """
        context = {
            'instances': Instance.objects.all()
        }
        return context
