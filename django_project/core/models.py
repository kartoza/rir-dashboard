from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _


class AbstractTerm(models.Model):
    """ Abstract model for Term """

    name = models.CharField(
        max_length=512, unique=True
    )
    description = models.TextField(
        null=True, blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class GeometryLevel(AbstractTerm):
    """
    Geometry level
    """
    lower_of = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True, null=True
    )


class Geometry(models.Model):
    """
    Geometry with it's type
    """
    identifier = models.CharField(
        max_length=512
    )
    name = models.CharField(
        max_length=512,
        null=True, blank=True
    )
    alias = models.TextField(
        blank=True, null=True,
        help_text=_(
            'Alias of the geometry name. '
            'Use comma separator for multi alias.')
    )
    geometry_level = models.ForeignKey(
        GeometryLevel,
        on_delete=models.CASCADE
    )
    geometry = models.MultiPolygonField(
        null=True, blank=True
    )
    child_of = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='geometry_child_of'
    )

    def __str__(self):
        return f'{self.name} ({self.identifier})'
