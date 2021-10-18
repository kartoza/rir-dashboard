from django.contrib.gis.db import models
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _
from rir_data.models.indicator import Indicator


class Harvester(models.Model):
    """ Harvester of indicator data
    """
    harvester_class = models.CharField(
        max_length=100,
        help_text=_(
            "The type of harvester that will be used."
            "Use class with full package.")
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
        from rir_data.models.harvester import HarvesterAttribute

        harvester = self.get_harvester_class
        for key, value in harvester.additional_attributes().items():
            HarvesterAttribute.objects.get_or_create(
                harvester=self,
                name=key,
                defaults={
                    'value': value
                }
            )

    def run(self):
        """
        Run the harvester
        """
        if self.active:
            self.get_harvester_class(self).run()
