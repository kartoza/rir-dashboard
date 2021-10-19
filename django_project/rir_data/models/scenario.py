from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from core.models import AbstractTerm


class ScenarioLevel(AbstractTerm):
    """
    The level of scenario
    """
    level = models.IntegerField(
        unique=True,
    )
    color = models.CharField(
        max_length=16,
        null=True, blank=True,
        help_text=_(
            'Put the hex color with # (e.g. #ffffff) '
            'or put the text of color. (e.g. blue)')
    )
    background_color = models.CharField(
        max_length=16,
        null=True, blank=True,
        help_text=_(
            'Put the hex color with # (e.g. #ffffff) '
            'or put the text of color. (e.g. blue)')
    )

    def __str__(self):
        return f'{self.level} - {self.name}'

    class Meta:
        ordering = ('level',)
