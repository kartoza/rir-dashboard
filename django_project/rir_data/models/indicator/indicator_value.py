from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from core.models import Geometry
from rir_data.models.indicator.indicator import Indicator


class IndicatorValue(models.Model):
    """
    The data of indicator
    It is saved per date
    """
    indicator = models.ForeignKey(
        Indicator, on_delete=models.CASCADE
    )
    date = models.DateField(
        _('Date'),
        help_text=_('The date of the value harvested.')
    )
    geometry = models.ForeignKey(
        Geometry, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    value = models.FloatField(
        help_text=_(
            'Use formula to create the rule and use x as the value.'
            'Example: x<100. '
            'It will replace x with the value and will check the condition.'
        )
    )

    class Meta:
        unique_together = ('indicator', 'date', 'geometry')
        ordering = ('-date',)
