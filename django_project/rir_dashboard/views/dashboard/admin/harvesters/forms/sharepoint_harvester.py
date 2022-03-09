import os
from django.conf import settings
from rir_harvester.harveters.sharepoint_harvester import SharepointHarvester
from ._base import HarvesterFormView


class SharepointHarvesterView(HarvesterFormView):
    harvester_class = SharepointHarvester
    template_name = 'dashboard/admin/harvesters/forms/sharepoint_harvester.html'

    @property
    def context_view(self) -> dict:
        """
        Return context for specific view by instance
        """
        context = super().context_view
        sharepoint_files = {}
        for (dirpath, dirnames, filenames) in os.walk(settings.ONEDRIVE_ROOT):
            if filenames:
                filenames.sort()
                for name in filenames:
                    if name.endswith(".xls") or name.endswith(".xlsx"):
                        sharepoint_files[name] = os.path.join(dirpath, name)
        context['files'] = sharepoint_files
        return context
