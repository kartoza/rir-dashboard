import os
import uuid
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _
from rir_data.models.indicator import Indicator

User = get_user_model()
APIWithGeographyAndTodayDate = (
    'rir_harvester.harveters.api_with_geography_and_today_date.APIWithGeographyAndTodayDate',
    'API With Geography Using Today Date',
)
APIListWithGeographyAndDate = (
    'rir_harvester.harveters.api_with_geography_and_date.APIWithGeographyAndDate',
    'API With Geography And Date',
)
UsingExposedAPI = (
    'rir_harvester.harveters.using_exposed_api.UsingExposedAPI',
    'Harvested using exposed API by external client',
)
ExcelHarvester = (
    'rir_harvester.harveters.excel_harvester.ExcelHarvester',
    'Excel Harvesters',
)
HARVESTERS = (
    APIWithGeographyAndTodayDate,
    APIListWithGeographyAndDate,
    UsingExposedAPI,
)
ALL_HARVESTERS = (
    APIWithGeographyAndTodayDate,
    APIListWithGeographyAndDate,
    UsingExposedAPI,
    ExcelHarvester,
)


class Harvester(models.Model):
    """ Harvester of indicator data
    """
    unique_id = models.UUIDField(
        default=uuid.uuid4, editable=False
    )
    harvester_class = models.CharField(
        max_length=256,
        help_text=_(
            "The type of harvester that will be used."
            "Use class with full package."),
        choices=ALL_HARVESTERS
    )
    indicator = models.OneToOneField(
        Indicator, on_delete=models.CASCADE,
        null=True, blank=True
    )
    is_run = models.BooleanField(
        default=False,
        help_text=_("Is the harvester running.")
    )
    active = models.BooleanField(
        default=True,
        help_text=_(
            'Make this harvester ready to be harvested.')
    )
    user = models.ForeignKey(
        User,
        null=True, blank=True,
        help_text=_(
            'User who run the harvester.'),
        on_delete=models.CASCADE
    )

    @property
    def get_harvester_class(self):
        return import_string(self.harvester_class)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.save_attributes()

    def save_attributes(self):
        """
        Save attributes for the harvesters
        """
        from rir_harvester.models import HarvesterAttribute
        harvester = self.get_harvester_class
        for key in harvester.additional_attributes().keys():
            HarvesterAttribute.objects.get_or_create(
                harvester=self,
                name=key
            )

    def run(self, force=False):
        """
        Run the harvester
        """
        if self.active:
            self.get_harvester_class(self).run(force)

    @property
    def report_file(self):
        folder = os.path.join(settings.MEDIA_ROOT, 'harvester', 'report')
        if not os.path.exists(folder):
            os.makedirs(folder)
        return os.path.join(folder, str(self.unique_id) + '.xlsx')

    @property
    def report_file_url(self):
        return os.path.join(settings.MEDIA_URL, 'harvester', 'report', str(self.unique_id) + '.xlsx')
