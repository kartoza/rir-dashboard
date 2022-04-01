from django.conf import settings
from rir_harvester.harveters.sharepoint_harvester import SharepointHarvester
from rir_dashboard.views.dashboard.admin.harvesters.forms._base import HarvesterFormView
from rir_data.utils import path_to_dict


class SharepointHarvesterView(HarvesterFormView):
    harvester_class = SharepointHarvester
    template_name = 'dashboard/admin/harvesters/forms/sharepoint_harvester.html'

    @property
    def context_view(self) -> dict:
        """
        Return context for specific view by instance
        """
        context = super().context_view
        context['dir'] = path_to_dict(settings.ONEDRIVE_ROOT, settings.ONEDRIVE_ROOT, ['.xlsx', '.xls'])
        return context
