import datetime
import requests
import traceback
from abc import ABC, abstractmethod
from django.contrib.auth import get_user_model
from django.utils import timezone
from rir_data.models import Geometry, IndicatorValue
from rir_data.models.indicator.indicator import IndicatorValueRejectedError
from rir_harvester.models import (
    Harvester, HarvesterLog, LogStatus
)

User = get_user_model()


class HarvestingError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class BaseHarvester(ABC):
    """ Abstract class for harvester """

    log = None
    description = ""
    attributes = {}
    mapping = {}
    done_message = ''

    def __init__(self, harvester: Harvester):
        self.harvester = harvester
        for attribute in harvester.harvesterattribute_set.all():
            self.attributes[attribute.name] = attribute.value if attribute.value else attribute.file
        for attribute in harvester.harvestermappingvalue_set.all():
            self.mapping[attribute.remote_value] = attribute.platform_value

        if harvester.indicator:
            self.reporting_units = harvester.indicator.reporting_units

    @staticmethod
    def additional_attributes(**kwargs) -> dict:
        """
        Attributes that needs to be saved on database
        The value is the default value for the attribute
        This will be used by harvester
        """
        return {}

    @property
    def _headers(self) -> dict:
        return {}

    def eval_json(self, json, str) -> dict:
        return eval(str.replace('x', 'json'))

    @abstractmethod
    def _process(self):
        """ Run the harvester process"""

    @property
    def allow_to_harvest_new_data(self):
        """
        Allowing if the new data can be harvested
        It will check based on the frequency
        """
        last_data = self.harvester.harvesterlog_set.all().first()
        if not last_data:
            return True

        difference = timezone.now() - last_data.start_time
        if self.harvester.indicator:
            return difference.days >= self.harvester.indicator.frequency.frequency
        else:
            return False

    def run(self, force=False):
        # run the process
        if self.allow_to_harvest_new_data or force:
            try:
                self.log = HarvesterLog.objects.create(harvester=self.harvester)
                # check the attributes
                for attr_key, attr_value in self.__class__.additional_attributes().items():
                    if attr_value.get('required', True):
                        if not self.attributes[attr_key]:
                            raise HarvestingError(f'{attr_key} is required and it is empty')

                self._process()
                self._done()
            except HarvestingError as e:
                self._error(f'{e}')
            except Exception:
                self._error(f'{traceback.format_exc().replace(" File", "<br>File")}')

    def _request_api(self, url: str):
        """ Request function"""
        try:
            response = requests.get(url, headers=self._headers)
            if response.status_code == 404:
                return {}
            response.raise_for_status()
            return response
        except (
                requests.exceptions.RequestException,
                requests.exceptions.HTTPError) as e:
            raise HarvestingError(f'{url} : {e}')

    def _error(self, message):
        self.harvester.is_run = False
        self.harvester.save()

        self.log.end_time = timezone.now()
        self.log.status = LogStatus.ERROR
        self.log.note = message
        self.log.save()

    def _done(self, message=''):
        self.harvester.is_run = False
        self.harvester.save()

        self.log.end_time = timezone.now()
        self.log.status = LogStatus.DONE
        self.log.note = message if message else self.done_message
        self.log.save()

    def _update(self, message=''):
        """ Update note for the log """
        self.log.note = message
        self.log.save()

    def save_indicator_data(self, value: str, date: datetime.date, geometry: Geometry) -> IndicatorValue:
        """ Save new indicator data of the indicator """
        try:
            if value:
                return self.harvester.indicator.save_value(date, geometry, float(value))
            else:
                return None
        except IndicatorValueRejectedError:
            return None
