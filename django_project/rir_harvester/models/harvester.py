from django.contrib.gis.db import models
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _
from rir_data.models.indicator import Indicator

APIListWithGeographyAndDate = (
    'rir_harvester.harveters.api_with_geography_and_date.APIWithGeographyAndDate',
    'API With Geography And Date',
)
HARVESTERS = (
    APIListWithGeographyAndDate,
)


class Harvester(models.Model):
    """ Harvester of indicator data
    """
    harvester_class = models.CharField(
        max_length=256,
        help_text=_(
            "The type of harvester that will be used."
            "Use class with full package."),
        choices=HARVESTERS
    )
    indicator = models.OneToOneField(
        Indicator, on_delete=models.CASCADE
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
