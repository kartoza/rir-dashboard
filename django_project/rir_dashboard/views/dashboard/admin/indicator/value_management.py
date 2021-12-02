import datetime
import json
from django.http import Http404
from django.shortcuts import redirect, reverse, render, get_object_or_404
from rir_dashboard.views.dashboard.admin._base import AdminView
from rir_data.models import Indicator, Instance, IndicatorValue, IndicatorExtraValue
from rir_data.serializer.geometry import GeometryContextSerializer


class IndicatorValueManagementMapView(AdminView):
    template_name = 'dashboard/admin/indicator/value-management-map.html'
    indicator = None

    @property
    def dashboard_title(self):
        return f'<span>Indicator Value Manager Map</span> : {self.indicator.name} '

    @property
    def context_view(self) -> dict:
        """
        Return context for specific view by instance
        """
        try:
            self.indicator = self.instance.indicators.get(
                id=self.kwargs.get('pk', '')
            )

            legends = {
                'NODATA': {
                    'name': 'No Data',
                    'color': 'gray'
                },
                'LATESTDATAFOUND': {
                    'name': 'Has Data',
                    'color': 'green'
                },
                'NEEDUPDATE': {
                    'name': 'Need Update Data',
                    'color': 'red'
                }
            }
            context = {
                'indicator': self.indicator,
                'geometry': json.loads(
                    json.dumps(
                        GeometryContextSerializer(
                            self.indicator.reporting_units,
                            many=True).data
                    )
                ),
                'geometry_has_updated_value': list(set(self.indicator.query_value(datetime.date.today()).values_list('geometry', flat=True))),
                'geometry_has_value': list(set(self.indicator.indicatorvalue_set.values_list('geometry', flat=True))),
                'legends': legends,
                'url_value_by_geometry': reverse('indicator-values-by-geometry', args=[
                    self.instance.slug, self.indicator.id, 0
                ])
            }
            return context
        except Indicator.DoesNotExist:
            raise Http404('Indicator does not found')


class IndicatorValueManagementTableView(AdminView):
    template_name = 'dashboard/admin/indicator/value-management-form.html'
    indicator = None

    @property
    def dashboard_title(self):
        return f'<span>Indicator Value Manager Form</span> : {self.indicator.name} '

    @property
    def context_view(self) -> dict:
        """
        Return context for specific view by instance
        """
        try:
            self.indicator = self.instance.indicators.get(
                id=self.kwargs.get('pk', '')
            )

            context = {
                'indicator': self.indicator,
                'geometry_reporting_units': self.indicator.reporting_units.order_by('name'),
                'values': self.indicator.indicatorvalue_set.order_by('date')
            }
            return context
        except Indicator.DoesNotExist:
            raise Http404('Indicator does not found')

    def post(self, request, **kwargs):
        self.instance = get_object_or_404(
            Instance, slug=kwargs.get('slug', '')
        )
        try:
            indicator = self.instance.indicators.get(
                id=self.kwargs.get('pk', '')
            )
            date = request.POST.get('date', None)
            if date:
                indicator_values = {}
                for reporting_unit in indicator.reporting_units:
                    try:
                        value = float(request.POST.get(f'{reporting_unit.id}', None))
                    except ValueError:
                        pass
                    else:
                        pass
                        try:
                            indicator_value = IndicatorValue.objects.get(
                                indicator=indicator,
                                date=date,
                                geometry=reporting_unit
                            )
                        except IndicatorValue.DoesNotExist:
                            indicator_value = IndicatorValue(
                                indicator=indicator,
                                date=date,
                                geometry=reporting_unit
                            )
                        indicator_value.value = value
                        indicator_value.save()
                        indicator_values[f'{reporting_unit.id}'] = indicator_value

                # we need to check extra value
                for key, extra_value in request.POST.dict().items():
                    if 'extra-value' in key:
                        keys = key.split('-')
                        reporting_id = keys[0]
                        extra_name = request.POST.get(f'{"-".join(keys[:3])}-name', None)
                        if extra_name and extra_value:
                            try:
                                indicator_value = indicator_values[reporting_id]
                                indicator_extra_value, created = IndicatorExtraValue.objects.get_or_create(
                                    indicator_value=indicator_value,
                                    name=extra_name
                                )
                                indicator_extra_value.value = extra_value
                                indicator_extra_value.save()
                            except KeyError:
                                pass

            return redirect(
                reverse(
                    'indicator-management-view', args=[self.instance.slug]
                )
            )
        except Indicator.DoesNotExist:
            raise Http404('Indicator does not found')
