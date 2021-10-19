import typing
from datetime import date
from django.db.models import Count, Sum
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from core.models import AbstractTerm, Geometry, GeometryLevel
from rir_data.models.scenario import ScenarioLevel
from rir_data.models.indicator.indicator_group import IndicatorGroup
from rir_data.models.indicator.indicator_frequency import IndicatorFrequency


# AGGREGATION BEHAVIOURS
class AggregationBehaviour(object):
    ALL_REQUIRED = 'All geography required in current time window'
    USE_AVAILABLE = 'Use all available populated geography in current time window'
    USE_MOST_RECENT = 'Most recent for each geography'


# AGGREGATION METHOD
class AggregationMethod(object):
    SUM = 'Aggregate data by sum all data.'
    MAJORITY = 'Aggregate data by majority data in the levels.'


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
    unit = models.CharField(
        max_length=256,
        default='',
        null=True, blank=True
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

    def scenario_rule(self, level):
        """
        Return scenario rule for specific level
        """
        scenario_rule = self.indicatorscenariorule_set.filter(scenario_level__level=level).first()
        if scenario_rule:
            return scenario_rule.rule
        return '-'

    def scenario_level(self, value) -> typing.Optional[ScenarioLevel]:
        """ Return scenario level of the value """
        if value:
            # check the rule
            for indicator_rule in self.indicatorscenariorule_set.all():
                try:
                    if eval(indicator_rule.rule.replace('x', f'{value}')):
                        return indicator_rule.scenario_level
                except NameError:
                    pass
        else:
            return None

    def values(self, geometry: Geometry, geometry_level: GeometryLevel, date_data: date):
        """
        Return geojson value of indicator by geometry, the target geometry level and the date
        """
        # get the geometries of data
        values = []
        query = self.indicatorvalue_set.filter(date__lte=date_data).filter(
            geometry__geometry_level=self.geometry_reporting_level
        )
        if not query.first():
            return values

        # update query by behaviour
        if self.aggregation_behaviour == AggregationBehaviour.USE_AVAILABLE:
            last_date = query.first().date
            query = query.filter(date=last_date)

        # get the geometries target by the level
        geometries_target = geometry.geometries_by_level(geometry_level)

        # get the data for every geometry target
        for geometry_target in geometries_target:
            geometries_report = list(
                geometry_target.geometries_by_level(
                    self.geometry_reporting_level).values_list('id', flat=True)
            )
            # filter data just by geometry target
            query_report = query.filter(
                geometry__in=geometries_report
            )
            try:
                value = None

                # aggregate the data by method
                if self.aggregation_method == AggregationMethod.MAJORITY:
                    output = query_report.values('value').annotate(
                        dcount=Count('value')
                    ).order_by('-dcount')
                    value = output[0]['value']
                elif self.aggregation_method == AggregationMethod.SUM:
                    output = query_report.values('value').annotate(
                        sum=Sum('value')
                    )
                    value = output[0]['sum']

                # return data
                scenario_value = self.scenario_level(value)
                values.append({
                    'geometry_id': geometry_target.id,
                    'geometry_identifier': geometry_target.identifier,
                    'geometry_name': geometry_target.name,
                    'value': value,
                    'scenario_value': scenario_value.level,
                    'color': scenario_value.background_color
                })
            except IndexError:
                pass

        return values
