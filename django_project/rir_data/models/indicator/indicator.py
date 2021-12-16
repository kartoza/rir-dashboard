import typing
from datetime import date
from django.db.models import Count, Sum
from django.contrib.gis.db import models
from django.shortcuts import reverse
from django.utils.translation import ugettext_lazy as _
from core.models.general import AbstractTerm
from rir_data.models.geometry import Geometry, GeometryLevelName
from rir_data.models.indicator.indicator_attributes import (
    IndicatorFrequency, IndicatorGroup
)
from rir_data.models.scenario import ScenarioLevel


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
    geometry_reporting_level = models.ForeignKey(
        GeometryLevelName, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    geometry_reporting_units = models.ManyToManyField(
        Geometry, blank=True
    )
    show_in_context_analysis = models.BooleanField(
        default=True,
        help_text=_(
            'Showing this indicator on Context Analysis.'
        )
    )
    unit = models.CharField(
        max_length=64,
        default=''
    )

    aggregation_behaviour = models.CharField(
        max_length=256,
        default=AggregationBehaviour.USE_AVAILABLE,
        choices=(
            # (AggregationBehaviour.ALL_REQUIRED, AggregationBehaviour.ALL_REQUIRED),
            (AggregationBehaviour.USE_AVAILABLE, AggregationBehaviour.USE_AVAILABLE),
            # (AggregationBehaviour.USE_MOST_RECENT, AggregationBehaviour.USE_MOST_RECENT)
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
    order = models.IntegerField(
        default=0
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('order',)

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
        return Indicator.objects.filter(show_in_context_analysis=True)

    def legends(self):
        """
        Return legend of indicator
        """
        output = {}
        for indicator_rule in self.indicatorscenariorule_set.all():
            output[indicator_rule.name] = {
                'color': indicator_rule.color if indicator_rule.color else indicator_rule.scenario_level.background_color,
                'level': indicator_rule.scenario_level.level

            }
        return output

    def scenario_rule(self, level):
        """
        Return scenario rule for specific level
        """
        return self.indicatorscenariorule_set.filter(
            scenario_level__level=level).first()

    def scenario_level(self, value) -> typing.Optional[ScenarioLevel]:
        """
        Return scenario level of the value
        """
        if value is not None:
            # check the rule
            for indicator_rule in self.indicatorscenariorule_set.all():
                try:
                    if eval(indicator_rule.rule.replace('x', f'{value}')):
                        return indicator_rule.scenario_level
                except NameError:
                    pass
        else:
            return None

    def query_value(self, date_data: date):
        """ Return query of value"""
        query = self.indicatorvalue_set.filter(date__lte=date_data).filter(
            geometry__geometry_level=self.geometry_reporting_level
        )

        # update query by behaviour
        if self.aggregation_behaviour == AggregationBehaviour.USE_AVAILABLE:
            if query.first():
                last_date = query.first().date
                query = query.filter(date=last_date)
        return query

    def serialize(self, geometry, value, attributes=None):
        # return data
        scenario_value = self.scenario_level(value)
        background_color = scenario_value.background_color if scenario_value else ''

        scenario_text = scenario_value.level if scenario_value else 0
        try:
            scenario_rule = self.scenario_rule(scenario_value.level)
            scenario_text = scenario_rule.name
            if scenario_rule and scenario_rule.color:
                background_color = scenario_rule.color
        except AttributeError:
            pass

        values = attributes if attributes else {}
        values.update({
            'geometry_id': geometry.id,
            'geometry_identifier': geometry.identifier,
            'geometry_name': geometry.name,
            'value': value,
            'scenario_value': scenario_value.level if scenario_value else 0,
            'scenario_text': scenario_text,
            'text_color': scenario_value.text_color if scenario_value else '',
            'background_color': background_color,
        })
        return values

    def values(self, geometry: Geometry, geometry_level: GeometryLevelName, date_data: date,
               use_exact_date=False, more_information=False):
        """
        Return list data based on the geometry and geometry level with date
        If it is upper than the reporting geometry level, it will be aggregate to upper level
        """
        from rir_data.models.indicator import IndicatorExtraValue

        # get the geometries of data
        values = []
        query = self.query_value(date_data)
        if use_exact_date:
            query = query.filter(date=date_data)

        reporting_units = list(self.reporting_units.values_list('id', flat=True))
        if not query.first():
            return values

        if geometry_level == self.geometry_reporting_level:
            # this is for returning real data
            query_report = query.filter(
                geometry__id__in=reporting_units
            )
            for indicator_value in query_report:
                attributes = {}
                if more_information:
                    attributes['date'] = indicator_value.date
                    attributes.update({
                        extra.name: extra.value for extra in indicator_value.indicatorextravalue_set.all()
                    })

                values.append(
                    self.serialize(
                        indicator_value.geometry,
                        indicator_value.value,
                        attributes
                    )
                )

        else:
            # this is for returning non real data
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
                ).filter(
                    geometry__id__in=reporting_units
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
                        output = query_report.values('indicator').annotate(
                            sum=Sum('value')
                        )
                        value = output[0]['sum']

                    # aggregate other value
                    attributes = {}
                    if more_information:
                        for extra_value in IndicatorExtraValue.objects.filter(
                                indicator_value__in=query_report.values_list('id', flat=True)):
                            try:
                                aggregated_value = int(extra_value.value)
                                if extra_value.name not in attributes:
                                    attributes[extra_value.name] = 0
                                attributes[extra_value.name] += aggregated_value
                            except ValueError:
                                pass

                    data = self.serialize(geometry_target, value, attributes)
                    if use_exact_date:
                        data['date'] = date_data
                    values.append(data)
                except IndexError as e:
                    print(e)
                    pass

        return values

    @property
    def reporting_units(self):
        """
        Return geometry of instance in the level when does not have geometry_reporting_units
        """
        if self.geometry_reporting_units.count() == 0:
            return self.group.instance.geometries().filter(
                geometry_level=self.geometry_reporting_level)
        else:
            return self.geometry_reporting_units.all()

    @property
    def url_geojson_template(self):
        instance = self.group.instance
        country_level = instance.geometry_instance_levels.filter(parent=None).first()
        if country_level:
            country_level = country_level.level
            geometry_country = instance.geometries().filter(
                geometry_level=country_level).first()
            if geometry_country:
                return reverse('indicator-values-by-date-geojson-api', args=[
                    self.group.instance.slug, self.pk,
                    geometry_country.identifier,
                    'level',
                    date.today()
                ])
        return None

    @property
    def url_data_template(self):
        instance = self.group.instance
        country_level = instance.geometry_instance_levels.filter(parent=None).first()
        if country_level:
            country_level = country_level.level
            geometry_country = instance.geometries().filter(
                geometry_level=country_level).first()
            if geometry_country:
                return reverse('indicator-values-by-date-api', args=[
                    self.group.instance.slug, self.pk,
                    geometry_country.identifier,
                    'level',
                    'date'
                ])
        return None

    @property
    def levels(self):
        """
        Return levels of indicators in tree
        """
        from rir_data.models import GeometryLevelInstance
        level_instance = GeometryLevelInstance.objects.filter(
            instance=self.group.instance,
            level=self.geometry_reporting_level
        ).first()
        if level_instance:
            return level_instance.get_level_tree()
        else:
            return []
