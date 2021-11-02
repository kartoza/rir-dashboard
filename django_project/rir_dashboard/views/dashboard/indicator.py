import json
from datetime import date
from django.http import Http404
from django.shortcuts import reverse
from rir_dashboard.views.dashboard._base import BaseDashboardView
from rir_data.models import Indicator


class IndicatorView(BaseDashboardView):
    template_name = 'dashboard/indicator.html'

    @property
    def dashboard_title(self):
        return 'Indicator'


class IndicatorMapView(BaseDashboardView):
    template_name = 'dashboard/indicator-map.html'
    indicator = None
    scenario_level = None

    @property
    def dashboard_title(self):
        element = self.scenario_level.element if self.scenario_level else ''
        return f'<span>Indicator Map</span> : {self.indicator.name} {element}'

    @property
    def context_view(self) -> dict:
        """
        Return context for specific view by instance
        """
        try:
            indicator = self.instance.indicators.get(
                id=self.kwargs.get('pk', '')
            )
            self.indicator = indicator
            levels = self.instance.geometry_levels_in_order

            legends = []
            for rule in indicator.indicatorscenariorule_set.order_by('scenario_level__level'):
                legends.append({
                    'name': rule.name,
                    'background_color': rule.scenario_level.background_color,
                    'text_color': rule.scenario_level.text_color,
                })

            context = {
                'indicator': indicator,
                'legends': legends
            }
            country_level = self.instance.geometry_levels.filter(parent=None).first()
            if country_level:
                country_level = country_level.level
                geometry_country = self.instance.geometries.filter(
                    geometry_level=country_level).first()
                if geometry_country:
                    context['country_geometry'] = json.loads(
                        geometry_country.geometry.geojson
                    )
                    values = indicator.values(
                        geometry_country,
                        country_level,
                        date.today()
                    )
                    try:
                        value = values[0]
                        self.scenario_level = self.instance.scenario_levels.get(level=value['scenario_value'])
                    except IndexError:
                        pass

                    # return the levels

                    level_with_url = {}
                    for level in levels:
                        level_with_url[level] = {
                            'level': level.name,
                            'url': reverse('indicator-values-geojson', args=[
                                self.instance.slug, indicator.pk, geometry_country.identifier, level, date.today()
                            ])
                        }
                        if indicator.geometry_reporting_level == level:
                            break
                    context['levels'] = level_with_url

            return context
        except Indicator.DoesNotExist:
            raise Http404('Indicator does not found')
