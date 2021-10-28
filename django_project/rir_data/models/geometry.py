from django.contrib.gis.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from core.models.general import AbstractTerm
from rir_data.models.instance import Instance


class GeometryLevelName(AbstractTerm):
    """
    Geometry level name
    """
    pass


class GeometryLevelInstance(models.Model):
    """
    This is geometry level hierarchy for the instance
    """
    instance = models.ForeignKey(
        Instance,
        on_delete=models.CASCADE
    )
    level = models.ForeignKey(
        GeometryLevelName,
        on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        GeometryLevelName,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='geometry_parent_level'
    )

    class Meta:
        unique_together = ('instance', 'level')


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
        max_length=512
    )
    instance = models.ForeignKey(
        Instance,
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=512
    )
    alias = models.TextField(
        default='',
        help_text=_(
            'Alias of the geometry name. '
            'Use comma separator for multi alias.')
    )
    geometry_level = models.ForeignKey(
        GeometryLevelName,
        on_delete=models.CASCADE
    )
    child_of = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='geometry_child_of'
    )
    geometry = models.MultiPolygonField()
    objects = FindGeometry()

    class Meta:
        unique_together = ('instance', 'identifier')
        verbose_name_plural = 'geometries'

    def __str__(self):
        return f'{self.name} ({self.identifier})'

    def geometries_by_level(self, geometry_level: GeometryLevelName):
        """
        Return geometries of this geometry by geometry level
        """
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