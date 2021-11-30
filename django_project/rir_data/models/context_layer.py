from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from core.models import AbstractTerm
from rir_data.models.instance import Instance


class LayerType(object):
    ARCGIS = 'ARCGIS'
    RASTER_TILE = 'Raster Tile'


class ContextLayerGroup(AbstractTerm):
    order = models.IntegerField(
        default=0
    )

    class Meta:
        ordering = ('order',)


class ContextLayer(AbstractTerm):
    instance = models.ForeignKey(
        Instance,
        on_delete=models.CASCADE
    )
    group = models.ForeignKey(
        ContextLayerGroup,
        null=True, blank=True,
        on_delete=models.SET_NULL
    )
    url = models.CharField(
        max_length=256
    )
    url_legend = models.CharField(
        max_length=256,
        null=True, blank=True
    )
    layer_type = models.CharField(
        max_length=256,
        default=LayerType.ARCGIS,
        choices=(
            (LayerType.ARCGIS, LayerType.ARCGIS),
            (LayerType.RASTER_TILE, LayerType.RASTER_TILE)
        )
    )
    show_on_map = models.BooleanField(
        default=True
    )
    enable_by_default = models.BooleanField(
        default=False
    )
    token = models.CharField(
        max_length=512,
        null=True, blank=True,
        help_text=_(
            "Token to access the layer"
        )
    )
    username = models.CharField(
        max_length=512,
        null=True, blank=True,
        help_text=_(
            "Username to access the layer"
        )
    )
    password = models.CharField(
        max_length=512,
        null=True, blank=True,
        help_text=_(
            "Password to access the layer"
        )
    )
    order = models.IntegerField(
        default=0
    )

    class Meta:
        ordering = ('order',)


class ContextLayerParameter(models.Model):
    """
    Additional parameter for context layer
    """
    context_layer = models.ForeignKey(
        ContextLayer, on_delete=models.CASCADE
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
        unique_together = ('context_layer', 'name')

    def __str__(self):
        return f'{self.name}'
