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


class AggregateMultiIndicatorAndGeometryAPIHarvester(BaseHarvester):
    """
    Harvest from API for multi indicator and geometry.
    Aggregate it by the value and save it to specific indicator.
    Indicator mapping will be <indicator name in remote>:<value> -> indicator on platform.
    The value will be number of data that found
    """
    description = (
        "Harvest from API for multi indicator and geometry. "
        "Aggregate it by the value and save it to specific indicator. "
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
                'description': "Username for authentication",
                'required': False
            },
            'password': {
                'title': "Password",
                'description': "Password for authentication",
                'type': 'password',
                'required': False
            },
            'instance_slug': {
                'title': "Slug of the instance",
                'description': "The instance slug of this harvester"
            },
            'key_geometry_list': {
                'title': "Key Name: Geometry List",
                'description': "The name of the key that contains geometry in a list",
                'type': 'select'
            },
            'key_geometry_value': {
                'title': "Key Name: Geometry",
                'description': "The name of the key that contains geometry value in geometry list",
                'type': 'select'
            },
            'key_indicator_list': {
                'title': "Key Name: Indicator List",
                'description': "The name of the key that contains indicator in a list",
                'type': 'select'
            },
            'key_indicator_value': {
                'title': "Key Name: Indicator",
                'description': "The name of the key that contains indicator value in indicator list",
                'type': 'select'
            },
            'key_date': {
                'title': "Key Name: Date",
                'description': "The name of the key that contains date",
                'type': 'select'
            },
            'date_format': {
                'description': (
                    "Format of the date from the data. "
                    "Check <a href='https://strftime.org/'>here</a>."
                    "Let it empty to use timestamp instead."
                ),
                'required': False
            },
            'key_value': {
                'title': "Key Name: Value",
                'description': "The name of the key that contains value",
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
        return

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
                            value = 1
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
