from django.contrib.gis.db import models
from django.db.models import Q
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


class FindGeometry(models.Manager):
    def get_by(self, name, geometry_level, child_of=None):
        return self.filter(
            child_of=child_of,
            geometry_level=geometry_level
        ).get(
            Q(name__iexact=name) |
            Q(alias__icontains=name)
        )


class Geometry(models.Model):
    """
    Geometry with it's type
    """
    identifier = models.CharField(
        max_length=512,
        unique=True
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
    objects = FindGeometry()

    def __str__(self):
        return f'{self.name} ({self.identifier})'

    def geometries_by_level(self, geometry_level: GeometryLevel):
        """ Return geometries of this geometry by geometry level """
        geometries = Geometry.objects.filter(id=self.id)
        current_geometry_level = self.geometry_level

        while geometry_level != current_geometry_level:
            geometry_ids = list(geometries.values_list('id', flat=True))
            geometries = Geometry.objects.filter(child_of__in=geometry_ids)

            if geometries.first():
                current_geometry_level = geometries.first().geometry_level
            else:
                current_geometry_level = geometry_level
        return geometries
