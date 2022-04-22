from rir_harvester.harveters.excel_harvester import ExcelHarvester
from rir_harvester.models.harvester import Harvester
from rir_harvester.tasks import run_harvester
from ._base import HarvesterFormView

MetaIngestor = (
    'rir_harvester.harveters.excel_harvester.ExcelHarvester',
    'Local Master File',
)


class MetaIngestorView(HarvesterFormView):
    harvester_class = ExcelHarvester
    template_name = 'dashboard/admin/harvesters/forms/meta_ingestor.html'

    @property
    def dashboard_title(self):
        return f'Meta Ingestor'

    def get_indicator(self):
        """
         Return indicator and save it as attribute
        """
        return None

    def get_harvester(self) -> Harvester:
        """
         Return harvester
        """
        uuid = self.kwargs.get('uuid', None)
        if not uuid:
            raise Harvester.DoesNotExist()
        return Harvester.objects.get(
            unique_id=uuid
        )

    @property
    def harvesters(self) -> tuple:
        """
         Return harvesters
        """
        return (MetaIngestor,)

    @property
    def context_view(self) -> dict:
        """
        Return context for specific view by instance
        """
        context = super().context_view
        for attr in context['attributes']:
            if attr['name'] == 'file':
                attr['title'] = 'File'
                attr['type'] = 'file'
                attr['description'] = 'Upload file that will be used to save the data'
                attr['file_accept'] = '.xlsx,.xls'
            if attr['name'] == 'instance_slug':
                attr['value'] = self.instance.slug
        return context

    def after_post(self, harvester: Harvester):
        """
         Called after post success
        """
        harvester.user = self.request.user
        harvester.save()
        run_harvester.delay(harvester.pk)
