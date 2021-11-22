import datetime
import requests
import traceback
from abc import ABC, abstractmethod
from django.contrib.auth import get_user_model
from rir_data.models import Geometry, IndicatorValue
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

    description = ""
    attributes = {}
    mapping = {}

    def __init__(self, harvester: Harvester):
        self.harvester = harvester
        self.reporting_units = harvester.indicator.reporting_units
        self.log = HarvesterLog.objects.create(harvester=harvester)
        for attribute in harvester.harvesterattribute_set.all():
            self.attributes[attribute.name] = attribute.value
        for attribute in harvester.harvestermappingvalue_set.all():
            self.mapping[attribute.remote_value] = attribute.platform_value

    @staticmethod
    def additional_attributes() -> dict:
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

    def run(self, force=False):
        # run the process
        try:
            self._process()
            self._done()

            # TODO:
            #  We need to make it forceable
            if self.harvester.indicator.allow_to_harvest_new_data or force:
                self._process()
                self._done()
            else:
                self._done("Harvesting can't be executed : still in the indicator frequency with last harvest time.")
        except HarvestingError as e:
            self._error(f'{e}')
        except Exception:
            self._error(f'{traceback.format_exc()}')

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

        self.log.end_time = datetime.datetime.now()
        self.log.status = LogStatus.ERROR
        self.log.note = message
        self.log.save()

    def _done(self, message=''):
        self.harvester.is_run = False
        self.harvester.save()

        self.log.end_time = datetime.datetime.now()
        self.log.status = LogStatus.DONE
        self.log.note = message
        self.log.save()

    def _update(self, message=''):
        """ Update note for the log """
        self.log.note = message
        self.log.save()

    def save_indicator_data(self, value: str, date: datetime.date, geometry: Geometry) -> IndicatorValue:
        """ Save new indicator data of the indicator """
        indicator_value, created = IndicatorValue.objects.get_or_create(
            indicator=self.harvester.indicator,
            date=date,
            geometry=geometry,
            defaults={
                'value': value
            }
        )
        indicator_value.value = value
        indicator_value.save()
        return indicator_value
