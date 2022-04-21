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
        return f'Harvester for {self.indicator.full_name}'

    def get_indicator(self):
        """
         Return indicator and save it as attribute
        """
        try:
            self.indicator = self.instance.indicators.get(
                id=self.kwargs.get('pk', '')
            )
            return self.indicator
        except Indicator.DoesNotExist:
            raise Http404('Indicator does not exist')

    def get_harvester(self) -> Harvester:
        """
         Return harvester
        """
        return self.indicator.harvester

    @property
    def harvesters(self) -> list:
        """
         Return harvesters
        """
        return HARVESTERS

    @property
    def context_view(self) -> dict:
        """
        Return context for specific view by instance
        """
        self.get_indicator()
        attributes = []
        mapping = []
        harvester = None
        try:
            harvester = self.get_harvester()
            for _map in harvester.harvestermappingvalue_set.order_by('remote_value'):
                mapping.append(
                    {
                        'remote_value': _map.remote_value,
                        'platform_value': _map.platform_value
                    }
                )
        except Harvester.DoesNotExist:
            pass

        harvester_class = str(self.harvester_class).split("'")[1]
        for name, attr in self.harvester_class.additional_attributes(
                instance=self.instance,
                indicator=self.indicator
        ).items():
            value = attr.get('value', '')
            try:
                if harvester:
                    value = harvester.harvesterattribute_set.get(name=name).value
            except HarvesterAttribute.DoesNotExist:
                pass

            attributes.append(
                {
                    'name': name,
                    'title': attr.get('title', name).replace('_', ' ').capitalize(),
                    'value': value if value else '',
                    'description': attr.get('description', ''),
                    'required': 'required' if 'required' not in attr or attr['required'] else '',
                    'type': attr.get('type', ''),
                    'class': attr.get('class', ''),
                    'data': attr.get('data', {}),
                    'read_only': attr.get('read_only', False),
                }
            )

        context = {
            'indicator': self.indicator,
            'harvesters': [
                {
                    'name': harvester[1],
                    'value': harvester[0],
                    'description': import_string(harvester[0]).description,
                    'url': reverse(
                        harvester[0], args=[self.instance.slug, self.indicator.id]
                    ) if self.indicator else ''
                } for harvester in self.harvesters
            ],
            'harvester_class': harvester_class,
            'attributes': attributes,
            'mapping': mapping
        }

        return context

    def after_post(self, harvester: Harvester):
        """
         Called after post success
        """
        pass

    def post(self, request, **kwargs):
        self.instance = get_object_or_404(
            Instance, slug=kwargs.get('slug', '')
        )
        indicator = self.get_indicator()
        try:
            data = request.POST.copy()
            data['attribute_extra_columns'] = ','.join(request.POST.getlist('attribute_extra_columns'))
            data['attribute_extra_keys'] = ','.join(request.POST.getlist('attribute_extra_keys'))
            harvester_class = data['harvester']
            try:
                harvester = self.get_harvester()
            except Harvester.DoesNotExist:
                if indicator:
                    harvester, created = Harvester.objects.get_or_create(
                        indicator=indicator,
                        defaults={
                            'harvester_class': harvester_class
                        }
                    )
                else:
                    harvester = Harvester.objects.create(
                        harvester_class=harvester_class
                    )

            harvester.harvesterattribute_set.all().delete()
            harvester.harvestermappingvalue_set.all().delete()

            harvester.harvester_class = harvester_class
            harvester.save()
            harvester.save_default_attributes(instance=self.instance)

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

            # this is for files
            for key, _file in request.FILES.items():
                if _file:
                    if 'attribute_' in key:
                        try:
                            attribute = harvester.harvesterattribute_set.get(
                                name=key.replace('attribute_', '')
                            )
                            attribute.file = _file
                            attribute.save()
                        except HarvesterAttribute.DoesNotExist:
                            pass

            self.after_post(harvester)
            if indicator:
                return redirect(
                    reverse(
                        'harvester-indicator-detail', args=[self.instance.slug, indicator.id]
                    )
                )
            else:
                return redirect(
                    reverse(
                        'harvester-detail', args=[self.instance.slug, str(harvester.unique_id)]
                    )
                )
        except KeyError as e:
            return HttpResponseBadRequest(f'{e} is required')
