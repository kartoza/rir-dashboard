from datetime import date
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from rir_data.models.geometry import GeometryLevelName
from rir_data.models.indicator.indicator_attributes import (
    IndicatorFrequency, IndicatorGroup
)


# AGGREGATION BEHAVIOURS
class AggregationBehaviour(object):
    ALL_REQUIRED = 'All geography required in current time window'
    USE_AVAILABLE = 'Use all available populated geography in current time window'
    USE_MOST_RECENT = 'Most recent for each geography'


# AGGREGATION METHOD
class AggregationMethod(object):
    SUM = 'Aggregate data by sum all data.'
    MAJORITY = 'Aggregate data by majority data in the levels.'


class Indicator(models.Model):
    """
    The indicator of scenario
    """
    name = models.CharField(
        max_length=512
    )
    group = models.ForeignKey(
        IndicatorGroup, on_delete=models.SET_NULL,
        blank=True, null=True
    )
    frequency = models.ForeignKey(
        IndicatorFrequency, on_delete=models.SET_NULL,
        blank=True, null=True
    )
    geometry_reporting_level = models.ForeignKey(
        GeometryLevelName, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    show_in_traffic_light = models.BooleanField(
        default=True,
        help_text=_(
            'Showing this indicator on traffic light.'
        )
    )

    aggregation_behaviour = models.CharField(
        max_length=256,
        default=AggregationBehaviour.USE_AVAILABLE,
        choices=(
            (AggregationBehaviour.ALL_REQUIRED, AggregationBehaviour.ALL_REQUIRED),
            (AggregationBehaviour.USE_AVAILABLE, AggregationBehaviour.USE_AVAILABLE),
            (AggregationBehaviour.USE_MOST_RECENT, AggregationBehaviour.USE_MOST_RECENT)
        )
    )

    aggregation_method = models.CharField(
        max_length=256,
        default=AggregationMethod.SUM,
        choices=(
            (AggregationMethod.SUM, AggregationMethod.SUM),
            (AggregationMethod.MAJORITY, AggregationMethod.MAJORITY)
        )
    )

    @property
    def allow_to_harvest_new_data(self):
        """
        Allowing if the new data can be harvested
        It will check based on the frequency
        """
        last_data = self.indicatorvalue_set.all().order_by('-date').first()
        if not last_data:
            return True

        difference = date.today() - last_data.date
        return difference.days >= self.frequency.frequency

    @staticmethod
    def list():
        """ Return list of indicators """
        return Indicator.objects.filter(show_in_traffic_light=True)
