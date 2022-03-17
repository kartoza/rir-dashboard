import requests
from base64 import b64encode
from datetime import datetime
from rir_harvester.harveters._base import (
    BaseHarvester, HarvestingError
)
from rir_data.models.geometry import Geometry
from rir_data.models.indicator.indicator import Indicator
from rir_data.models.indicator.indicator_value import (
    IndicatorValue, IndicatorValueExtraDetailColumn, IndicatorValueExtraDetailRow
)


class EtoolsProgramCoverageHarvester(BaseHarvester):
    """
    Harvester program coverage data from etools
    """
    description = (
        "Harvest program coverage data from etools. <br>"
        "It use sections as the indicator and locations_data as geometry on the API data"
    )

    @staticmethod
    def additional_attributes(**kwargs) -> dict:
        attr = {
            'url': {
                'title': "URL",
                'description': "The url of file that will be downloaded to be harvested"
            },
            'username': {
                'title': "Username",
                'description': "Username for authentication"
            },
            'password': {
                'title': "Password",
                'description': "Password for authentication",
                'type': 'password'
            },
            'instance_slug': {
                'title': "Slug of the instance",
                'description': "The instance slug of this harvester"
            },
            'key_value': {
                'title': "Key Name: Value",
                'description': "The name of the keys that contains value",
                'type': 'select'
            },
            'extra_keys': {
                'title': "Keys for the extra data",
                'description': "List of keys as extra data",
                'required': False,
                'type': 'select'
            },
        }
        return attr

    def _process(self):
        """ Run the harvester """

        self._update('Fetching data')
        user = f"{self.attributes['username']}:{self.attributes['password']}"
        user = bytes(user, 'utf-8')
        headers = {
            'Authorization': 'Basic %s' % b64encode(user).decode("ascii")
        }
        response = requests.get(self.attributes['url'], headers=headers)
        if response.status_code is not 200:
            raise HarvestingError(response.content)

        results = response.json()['results']
        total = len(results)

        for mapping, value in self.mapping.items():
            try:
                indicator_identifier = value.split('/')
                indicator = Indicator.objects.get(
                    group__name=indicator_identifier[0],
                    name=indicator_identifier[1],
                )
                IndicatorValue.objects.filter(indicator=indicator).delete()
            except (Indicator.DoesNotExist, IndexError):
                pass

        for idx, result in enumerate(results):
            self._update(f'Processing data {idx}/{total}')

            # TODO:
            #  Fix which data should we use
            try:
                # date = datetime.strptime(result['created'], "%d %b %Y %H:%M:%S").date()
                date = datetime.now().date()
                sections = result['sections'].split(',')
                # we check per indicator
                for section in sections:
                    try:
                        indicator_identifier = self.mapping[section].split('/')
                        indicator = Indicator.objects.get(
                            group__name=indicator_identifier[0],
                            name=indicator_identifier[1],
                        )

                        # check the value
                        value = result[self.attributes['key_value']]
                        if value is None or value == '':
                            result.append(f'{indicator.name} : Value is empty')
                        else:
                            try:
                                if float(value) < indicator.min_value or float(value) > indicator.max_value:
                                    value = 1
                            except ValueError:
                                rule = indicator.indicatorscenariorule_set.filter(name__iexact=value).first()
                                if rule:
                                    value = float(rule.rule.replace(' ', '').replace('x==', ''))
                                else:
                                    value = 1

                        for location_data in result['locations_data']:
                            try:
                                geometry = indicator.reporting_units.get(identifier=location_data['pcode'])
                                value = float(value)
                                indicator_value, created = IndicatorValue.objects.get_or_create(
                                    indicator=indicator, date=date, geometry=geometry,
                                    defaults={
                                        'value': value
                                    }
                                )
                                indicator_value.value = value
                                indicator_value.save()

                                # save details data
                                row = IndicatorValueExtraDetailRow.objects.create(
                                    indicator_value=indicator_value
                                )
                                for extra in self.attributes['extra_keys'].split(','):
                                    if extra in result and result[extra]:
                                        IndicatorValueExtraDetailColumn.objects.get_or_create(
                                            row=row,
                                            name=extra,
                                            defaults={
                                                'value': result[extra]
                                            }
                                        )


                            except Geometry.DoesNotExist:
                                pass
                    except (IndexError, KeyError, Indicator.DoesNotExist):
                        pass
            except ValueError:
                raise HarvestingError('Date is not in format %Y-%m-%d')

    @staticmethod
    def get_harvester(instance):
        from rir_harvester.models.harvester import EtoolsProgramCoverageHarvesterTuple
        from rir_harvester.models.harvester_attribute import (
            HarvesterAttribute
        )

        attribute = HarvesterAttribute.objects.filter(
            name='instance_slug',
            value=instance.slug,
            harvester__indicator=None,
            harvester__harvester_class=EtoolsProgramCoverageHarvesterTuple[0]
        ).first()
        if attribute:
            return attribute.harvester
        return None
