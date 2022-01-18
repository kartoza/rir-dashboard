from collections import OrderedDict
from datetime import datetime
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get, save_data
from django.utils.timezone import now
from rir_harvester.harveters._base import (
    BaseHarvester, HarvestingError
)
from rir_data.models import (
    Instance, Geometry, Indicator, IndicatorValue, IndicatorExtraValue
)


class ExcelHarvester(BaseHarvester):
    """
    Harvester just get the data from api and has list and
    map the geography name with data
    """
    description = (
        "Harvest data from spreadsheet for multi indicator. "
        "<br>Create data in the spreadsheet with the name of indicator as the column name."
        "<br>Select what sheet name should be use and select what column name that will be used for specific indicator."
    )

    @staticmethod
    def additional_attributes(**kwargs) -> dict:
        attr = {
            'date': {
                'title': "Date of Data",
                'description': "The date for the data that will be used.",
                'required': False,
                'type': 'date'
            },
            'file': {
                'title': "URL of file",
                'description': "The url of file that will be downloaded to be harvested"
            },
            'sheet_name': {
                'title': "Sheet name",
                'description': "Sheet that will be used"
            },
            'column_name_administration_code': {
                'title': "Column Name: Administration Code",
                'description': "The name of column in the file contains administration code"
            },
            'instance_slug': {
                'title': "Slug of the instance",
                'description': "The instance slug of this harvester"
            },
        }
        try:
            instance = kwargs['instance']
            for indicator in instance.indicators:
                attr[indicator.name] = {
                    'title': "Column Name: " + indicator.name,
                    'description': indicator.description,
                    'class': 'indicator-name',
                    'required': False,
                    'data': {
                        'name': indicator.name,
                        'description': indicator.description,
                        'shortcode': indicator.shortcode if indicator.shortcode else '',
                    }
                }
        except KeyError:
            pass
        return attr

    def get_records(self):
        """ Get records form upload session """
        _file = self.harvester.harvesterattribute_set.get(name='file').file

        records = []
        if _file:
            _file.seek(0)
            sheet = None
            if str(_file).split('.')[-1] == 'xls':
                sheet = xls_get(_file)
            elif str(_file).split('.')[-1] == 'xlsx':
                sheet = xlsx_get(_file)
            if sheet:
                try:
                    records = sheet[self.attributes.get('sheet_name', '')]
                except KeyError:
                    raise HarvestingError(f'Sheet name : {self.attributes.get("sheet_name", "")} does not exist.')
        return records

    def _process(self):
        """ Run the harvester """

        # fetch data
        self._update('Fetching data')
        records = self.get_records()
        try:
            instance = Instance.objects.get(slug=self.attributes['instance_slug'])
        except Instance.DoesNotExist:
            raise HarvestingError('The instance is not found, please reupload.')

        # get keys
        indicators_column = {}
        key_column_name_administration_code = None
        try:
            key_column_name_administration_code = records[0].index(self.attributes['column_name_administration_code'])
        except ValueError as e:
            if 'not in list' in str(e):
                raise HarvestingError(str(e).replace('is not in list', '') + ' column is not found')

        for indicator in instance.indicators:
            try:
                indicators_column[records[0].index(self.attributes[indicator.name])] = indicator
            except ValueError:
                pass

        # date
        date = now().date()
        if self.attributes['date']:
            try:
                date = datetime.strptime(self.attributes['date'], "%Y-%m-%d").date()
            except ValueError:
                raise HarvestingError('Date is not in format %Y-%m-%d')

        # process data
        total = len(records[1:])
        output_records = []
        geometries = {}
        for idx, record in enumerate(records[1:]):
            self._update(f'Processing line {idx + 2}/{total + 2}')
            administrative_code = record[key_column_name_administration_code]

            # we check the values per indicator
            result = []
            for idx, indicator in indicators_column.items():
                value = record[idx]
                try:
                    if not value:
                        result.append(f'{indicator.name} : Value is empty')
                    else:
                        try:
                            if float(value) < indicator.min_value or float(value) > indicator.max_value:
                                result.append(f'{indicator.name} : Value is not between {indicator.min_value}-{indicator.max_value}')
                                continue
                        except ValueError:
                            rule = indicator.indicatorscenariorule_set.filter(name__iexact=value).first()
                            if not rule:
                                result.append(f'{indicator.name} : Value is not recognized')
                                continue
                            value = float(rule.rule.replace(' ', '').replace('x==', ''))

                        geometry = geometries[administrative_code] if administrative_code in geometries \
                            else indicator.reporting_units.get(identifier=administrative_code)
                        value = float(value)
                        indicator_value, created = IndicatorValue.objects.get_or_create(
                            indicator=indicator, date=date, geometry=geometry,
                            defaults={
                                'value': value
                            }
                        )
                        indicator_value.value = value
                        indicator_value.save()
                        result.append(f'{indicator.name} :' + ('Created' if created else 'Replaced'))
                except Indicator.DoesNotExist:
                    result.append(f'{indicator.name} : Indicator does not exist')
                except Geometry.DoesNotExist:
                    result.append(f'{indicator.name} : Geometry does not exist')
                except ValueError:
                    result.append(f'{indicator.name} : Value is not a number')
                except TypeError:
                    result.append(f'{indicator.name} : Date format is not Year-Month-Day')
            output_records.append([', '.join(result)] + record)

        output_records = [['Result'] + records[0]] + output_records

        # save output reports to excel file
        data = OrderedDict()
        data.update(
            {"output": output_records}
        )
        save_data(self.harvester.report_file, data)
        self.done_message = f'Please check the report in this <a href="{self.harvester.report_file_url}">REPORT FILE</a>'
