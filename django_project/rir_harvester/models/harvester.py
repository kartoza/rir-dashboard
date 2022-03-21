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
SharepointHarvester = (
    'rir_harvester.harveters.sharepoint_harvester.SharepointHarvester',
    'Sharepoint File',
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
    SharepointHarvester,
    UsingExposedAPI,
)
ALL_HARVESTERS = HARVESTERS + (
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

    def __str__(self):
        return str(self.unique_id)

    @property
    def get_harvester_class(self):
        return import_string(self.harvester_class)

    @property
    def harvester_name(self):
        for harvester in ALL_HARVESTERS:
            if harvester[0] == self.harvester_class:
                return harvester[1]
        return ''

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.save_attributes()

    def save_attributes(self, **kwargs):
        """
        Save attributes for the harvesters
        """
        from rir_harvester.models import HarvesterAttribute
        harvester = self.get_harvester_class
        for key in harvester.additional_attributes(**kwargs).keys():
            HarvesterAttribute.objects.get_or_create(
                harvester=self,
                name=key
            )

    def get_attributes(self):
        """
        Get attributes keys
        """
        from rir_harvester.models import HarvesterAttribute
        ids = []
        attributes = []
        for attribute in self.get_harvester_class.additional_attributes().keys():
            try:
                attr = self.harvesterattribute_set.get(name=attribute)
                if attr.value:
                    attributes.append(attr)
                    ids.append(attr.id)
            except HarvesterAttribute.DoesNotExist:
                pass
        for attr in self.harvesterattribute_set.exclude(id__in=ids):
            if attr.value:
                attributes.append(attr)
        return attributes

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
