from django.contrib.gis.db import models
from core.models.general import AbstractTerm


class Instance(AbstractTerm):
    """
    Instance model
    """
    icon = models.FileField(
        upload_to='instance/icons',
        null=True,
        blank=True
    )
