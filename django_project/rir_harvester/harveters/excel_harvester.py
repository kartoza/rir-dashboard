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
        "Create data per sheet with the name of indicator as the sheet name."
        "<br>The date will be used are:"
        "<br>1. Using date in <b>Column Name: Date</b> if it is present."
        "<br>2. If not present, it will use <b>Date of Data</b>"
        "<br>3. If not provided, it will use the current data."
    )

    @staticmethod
    def additional_attributes() -> dict:
        return {
            'file': {
                'title': "URL of file",
                'description': "The url of file that will be downloaded to be harvested"
            },
            'column_name_administration_code': {
                'title': "Column Name: Administration Code",
                'description': "The name of column in the file contains administration code"
            },
            'column_name_indicator': {
                'title': "Column Name: Indicator Name",
                'description': "The name of column in the file contains indicator name"
            },
            'column_name_value': {
                'title': "Column Name: Value",
                'description': "The name of column in the file contains value"
            },
            'column_name_date': {
                'title': "Column Name: Date",
                'description': "The name of column in the file contains date",
                'required': False
            },
            'extra_columns': {
                'title': "Extra Columns",
                'description': "Put the column names as extra data with comma separator. It will save those columns as extra data.",
                'required': False
            },
            'date': {
                'title': "Date of Data",
                'description': "The date for the data that will be used.",
                'required': False,
                'type': 'date'
            },
            'instance_slug': {
                'title': "Slug of the instance",
                'description': "The instance slug of this harvester"
            },
        }

    def get_records(self):
        """ Get records form upload session """
        _file = self.harvester.harvesterattribute_set.get(name='file').file

        records = []
        if _file:
            _file.seek(0)
            sheet = None
            if str(_file).split('.')[-1] == 'xls':
                sheet = xls_get(_file, column_limit=20)
            elif str(_file).split('.')[-1] == 'xlsx':
                sheet = xlsx_get(_file, column_limit=20)
            if sheet:
                sheet_name = next(iter(sheet))
                records = sheet[sheet_name]
        return records

    def _process(self):
        """ Run the harvester """

        # fetch data
        self._update('Fetching data')
        attribute = self.harvester.harvesterattribute_set.get(name='file')
        records = self.get_records()
        try:
            instance = Instance.objects.get(slug=self.attributes['instance_slug'])
        except Instance.DoesNotExist:
            raise HarvestingError('The instance is not found, please reupload.')

        # get keys
        key_extra_column = {}
        key_column_name_date = None
        try:
            key_column_name_administration_code = records[0].index(self.attributes['column_name_administration_code'])
            key_column_name_indicator = records[0].index(self.attributes['column_name_indicator'])
            key_column_name_value = records[0].index(self.attributes['column_name_value'])
            if self.attributes['column_name_date']:
                key_column_name_date = records[0].index(self.attributes['column_name_date'])
            if self.attributes['extra_columns']:
                for column in self.attributes['extra_columns'].split(','):
                    key_extra_column[column] = records[0].index(column)
        except ValueError as e:
            if 'not in list' in str(e):
                raise HarvestingError(str(e).replace('is not in list', '') + ' column is not found')
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
        indicators = {}
        geometries = {}
        for idx, record in enumerate(records[1:]):
            self._update(f'Processing line {idx + 2}/{total + 2}')
            administrative_code = record[key_column_name_administration_code]
            indicator_name = record[key_column_name_indicator]
            value = record[key_column_name_value]

            if not value:
                result = 'Skip : Value is empty'
            else:
                try:
                    if key_column_name_date:
                        date = datetime.strptime(record[key_column_name_date], "%Y-%m-%d").date()

                    indicator = indicators[indicator_name] if indicator_name in indicators \
                        else instance.indicators.get(name=indicator_name)
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

                    for name, index in key_extra_column.items():
                        try:
                            extra_value, created = IndicatorExtraValue.objects.get_or_create(
                                indicator_value=indicator_value,
                                name=name,
                                defaults={
                                    'value': str(record[index])
                                }
                            )
                            extra_value.value = str(record[index])
                            extra_value.save()
                        except IndexError:
                            pass
                    result = 'Created' if created else 'Replaced'
                except Indicator.DoesNotExist:
                    result = 'Indicator does not exist'
                except Geometry.DoesNotExist:
                    result = 'Geometry does not exist'
                except ValueError:
                    result = 'Value is not a number'
                except TypeError:
                    result = 'Date format is not Year-Month-Day'
            output_records.append([result] + record)

        output_records = [['Result'] + records[0]] + output_records

        # save output reports to excel file
        data = OrderedDict()
        data.update(
            {"output": output_records}
        )
        save_data(self.harvester.report_file, data)
        self.done_message = f'Please check the result in this <a href="{self.harvester.report_file_url}">FILE</a>'
