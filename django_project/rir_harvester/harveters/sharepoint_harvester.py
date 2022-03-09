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


class SharepointHarvester(BaseHarvester):
    """
    Harvester using sharepoint file in the volume settings.ONEDRIVE_ROOT
    """
    description = (
        "Harvester using sharepoint file. <br>"
        "It will fetch the data from file and the file synced frequently."
    )

    @staticmethod
    def additional_attributes(**kwargs) -> dict:
        attr = {
            'file': {
                'title': "Path of file",
                'description': "The path of file in the server."
            },
            'sheet_name': {
                'title': "Sheet name",
                'description': "Sheet that will be used"
            },
            'row_number_for_header': {
                'title': "Row Number: Header",
                'description': "Row number that will be used as header."
            },
            'column_name_administration_code': {
                'title': "Column Name: Administration Code",
                'description': "The name of column in the file contains administration code"
            },
            'column_name_month': {
                'title': "Column Name: Month",
                'description': "The name of column in the file contains month data"
            },
            'column_name_year': {
                'title': "Column Name: Year",
                'description': "The name of column in the file contains year data"
            },
            'column_name_value': {
                'title': "Column Name: Value",
                'description': "The name of column in the file contains year data"
            },
            'extra_columns': {
                'title': "Columns Name: Extra Data",
                'description': "List of columns as extra data",
                'required': False
            },
        }
        return attr

    def _process(self):
        """ Run the harvester """
        return
