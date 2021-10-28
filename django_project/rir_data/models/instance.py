from django.contrib.gis.db import models
from core.models.general import SlugTerm


class Instance(SlugTerm):
    """
    Instance model
    """
    icon = models.FileField(
        upload_to='instance/icons',
        null=True,
        blank=True
    )

    @property
    def scenarios(self):
        return self.scenariolevel_set.all()

    @property
    def indicator_groups(self):
        return self.indicatorgroup_set.all()

    @property
    def geometry_levels(self):
        return self.geometrylevelinstance_set.all()

    @property
    def programs(self):
        return self.program_set.all()

    @property
    def geometries(self):
        return self.geometry_set.all()
