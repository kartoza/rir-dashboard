import typing
from datetime import date
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from core.models import AbstractTerm, GeometryLevel, Geometry
from scenario.models.scenario import ScenarioLevel


class IndicatorGroup(AbstractTerm):
    """
    The group of indicator
    """
    pass


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


class Indicator(AbstractTerm):
    """
    The indicator of scenario
    """
    group = models.ForeignKey(
        IndicatorGroup, on_delete=models.SET_NULL,
        blank=True, null=True
    )
    frequency = models.ForeignKey(
        IndicatorFrequency, on_delete=models.SET_NULL,
        blank=True, null=True
    )
    show_in_traffic_light = models.BooleanField(
        default=True,
        help_text=_(
            'Showing this indicator on traffic light.'
        )
    )
    geometry_reporting_level = models.ForeignKey(
        GeometryLevel, on_delete=models.SET_NULL,
        null=True, blank=True
    )

    @property
    def allow_to_harvest_new_data(self):
        """
        Allowing if the new data can be harvested
        It will check based on the frequency
        """
        last_data = self.harvester.indicator.indicatorvalue_set.all().order_by('-date').first()
        if not last_data:
            return True

        difference = date.today() - last_data.date
        return difference.days >= self.frequency.frequency

    @property
    def value(self):
        first_data = self.indicatorvalue_set.first()
        if not first_data:
            return None
        return first_data.value

    @property
    def scenario_level(self) -> typing.Optional[ScenarioLevel]:
        """ Return scenario level of the value """
        value = self.value
        if value:
            # check the rule
            for indicator_rule in self.indicatorscenariorule_set.all():
                try:
                    if eval(indicator_rule.rule.replace('x', value)):
                        return indicator_rule.scenario_level
                except NameError:
                    pass
        else:
            return None

    @staticmethod
    def list():
        """ Return list of indicators """
        return Indicator.objects.filter(show_in_traffic_light=True)


class IndicatorScenarioRule(models.Model):
    """
    The rule of scenario
    """
    name = models.CharField(
        max_length=512
    )
    indicator = models.ForeignKey(
        Indicator,
        on_delete=models.CASCADE
    )
    scenario_level = models.ForeignKey(
        ScenarioLevel,
        on_delete=models.CASCADE
    )
    rule = models.CharField(
        max_length=256,
        help_text=_(
            'Use formula to create the rule and use x as the value.'
            'Example: x<100. '
            'It will replace x with the value and will check the condition.'
        )
    )

    class Meta:
        unique_together = ('indicator', 'scenario_level')


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
    value = models.CharField(
        max_length=256,
        help_text=_(
            'Use formula to create the rule and use x as the value.'
            'Example: x<100. '
            'It will replace x with the value and will check the condition.'
        )
    )

    class Meta:
        unique_together = ('indicator', 'date', 'geometry')
        ordering = ('-date',)
