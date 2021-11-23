from django.http import Http404, HttpResponseBadRequest
from django.utils.module_loading import import_string
from django.shortcuts import get_object_or_404, redirect, reverse
from rir_dashboard.views.dashboard.admin._base import AdminView
from rir_data.models import Indicator, Instance
from rir_harvester.models import (
    HARVESTERS, Harvester, HarvesterAttribute, HarvesterMappingValue
)


class HarvesterFormView(AdminView):
    indicator = None
    harvester_class = None

    @property
    def dashboard_title(self):
        return f'Harvester for {self.indicator.__str__()}'

    @property
    def context_view(self) -> dict:
        """
        Return context for specific view by instance
        """
        try:
            self.indicator = self.instance.indicators.get(
                id=self.kwargs.get('pk', '')
            )
        except Indicator.DoesNotExist:
            raise Http404('Indicator does not found')

        attributes = []
        mapping = []
        harvester = None
        try:
            harvester = self.indicator.harvester
            for _map in harvester.harvestermappingvalue_set.all():
                mapping.append(
                    {
                        'remote_value': _map.remote_value,
                        'platform_value': _map.platform_value
                    }
                )
        except Harvester.DoesNotExist:
            pass

        harvester_class = str(self.harvester_class).split("'")[1]
        if harvester and harvester.harvester_class != harvester_class:
            raise Http404('Harvester does not match')

        for name, description in self.harvester_class.additional_attributes().items():
            value = ''
            if harvester:
                value = harvester.harvesterattribute_set.get(name=name).value
            attributes.append(
                {
                    'name': name,
                    'title': name.replace('_', ' ').capitalize(),
                    'value': value if value else '',
                    'description': description
                }
            )

        context = {
            'indicator': self.indicator,
            'harvesters': [
                {
                    'name': harvester[1],
                    'value': harvester[0],
                    'description': import_string(harvester[0]).description
                } for harvester in HARVESTERS
            ],
            'harvester_class': harvester_class,
            'attributes': attributes,
            'mapping': mapping
        }
        return context

    def post(self, request, **kwargs):
        self.instance = get_object_or_404(
            Instance, slug=kwargs.get('slug', '')
        )
        try:
            indicator = self.instance.indicators.get(
                id=self.kwargs.get('pk', '')
            )
        except Indicator.DoesNotExist:
            raise Http404('Indicator does not found')
        try:
            data = request.POST
            harvester_class = data['harvester']
            harvester, created = Harvester.objects.get_or_create(
                indicator=indicator,
                defaults={
                    'harvester_class': harvester_class
                }
            )
            harvester.harvesterattribute_set.all().delete()
            harvester.harvestermappingvalue_set.all().delete()

            harvester.harvester_class = harvester_class
            harvester.save()
            harvester.save_attributes()

            for key, value in data.items():
                if value:
                    if 'attribute_' in key:
                        try:
                            attribute = harvester.harvesterattribute_set.get(
                                name=key.replace('attribute_', '')
                            )
                            attribute.value = value
                            attribute.save()
                        except HarvesterAttribute.DoesNotExist:
                            pass
                    if 'mapping_remote_' in key:
                        try:
                            mapping_id = key.replace('mapping_remote_', '')
                            mapping_remote = value
                            mapping_platform = data['mapping_platform_' + mapping_id]
                            HarvesterMappingValue.objects.get_or_create(
                                harvester=harvester,
                                remote_value=mapping_remote,
                                defaults={
                                    'platform_value': mapping_platform
                                }
                            )
                        except KeyError:
                            pass

            return redirect(
                reverse(
                    'indicator-management-view', args=[self.instance.slug]
                )
            )
        except KeyError as e:
            return HttpResponseBadRequest(f'{e} is required')
