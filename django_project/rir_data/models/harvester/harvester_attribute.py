from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from rir_data.models.harvester import Harvester


class HarvesterAttribute(models.Model):
    """
    Additional attribute for harvester
    """
    harvester = models.ForeignKey(
        Harvester, on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=100,
        help_text=_(
            "The name of attribute"
        )
    )
    value = models.TextField(
        null=True, default=True,
        help_text=_(
            "The value of attribute"
        )
    )

    class Meta:
        unique_together = ('harvester', 'name')

    def __str__(self):
        return f'{self.name}'
