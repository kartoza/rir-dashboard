from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from core.models import AbstractTerm
from rir_data.models.instance import Instance


class IndicatorFrequency(AbstractTerm):
    """
    The frequency of data for the indicator
    """
    frequency = models.IntegerField(
        help_text=_(
            'Frequency in days. '
            'This is used by harvester as a frequency to get new indicator data.'
        )
    )

    class Meta:
        verbose_name_plural = 'indicator frequencies'


class IndicatorGroup(AbstractTerm):
    """
    The group of indicator
    It is linked with the instance
    """
    instance = models.ForeignKey(
        Instance,
        on_delete=models.CASCADE
    )
