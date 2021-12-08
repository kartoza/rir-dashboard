from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from core.models import AbstractTerm, IconTerm
from rir_data.models.instance import Instance


class BasemapLayer(AbstractTerm, IconTerm):
    instance = models.ForeignKey(
        Instance,
        on_delete=models.CASCADE
    )
    url = models.CharField(
        max_length=256
    )
    show_on_map = models.BooleanField(
        default=True
    )
    enable_by_default = models.BooleanField(
        default=False
    )

    class Meta:
        ordering = ('name',)


class BasemapLayerParameter(models.Model):
    """
    Additional parameter for basemap layer
    """
    basemap_layer = models.ForeignKey(
        BasemapLayer, on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=128,
        help_text=_(
            "The name of parameter"
        )
    )
    value = models.CharField(
        max_length=128,
        null=True, blank=True,
        help_text=_(
            "The value of parameter"
        )
    )

    class Meta:
        unique_together = ('basemap_layer', 'name')

    def __str__(self):
        return f'{self.name}'
