import responses
import datetime
from django.test.testcases import TestCase
from rir_data.tests.model_factories import IndicatorF, InstanceF, IndicatorGroupF, GeometryLevelNameF, GeometryF
from rir_harvester.models.harvester import APIListWithGeographyAndDate, Harvester
from rir_harvester.tests.model_factories import HarvesterF


class APIWithGeograpyAndDate(TestCase):
    """ Test for Harvester : APIWithGeograpyAndDate """

    def setUp(self):
        instance = InstanceF()
        level = GeometryLevelNameF()
        indicator = IndicatorF(
            group=IndicatorGroupF(
                instance=instance
            ),
            geometry_reporting_level=level
        )

        GeometryF(
            identifier='A',
            instance=instance,
            geometry_level=level
        )

        GeometryF(
            identifier='B',
            instance=instance,
            geometry_level=level
        )

        GeometryF(
            identifier='C',
            instance=instance,
            geometry_level=level
        )

        self.harvester = HarvesterF(
            indicator=indicator,
            harvester_class=APIListWithGeographyAndDate[0]
        )

    def test_no_attr_error(self):
        self.harvester.run()
        log = self.harvester.harvesterlog_set.last()
        self.assertEqual(log.status, 'Error')
        self.assertEqual(
            log.note, list(
                self.harvester.get_harvester_class.additional_attributes().keys()
            )[0] + ' is required and it is empty'
        )

    @responses.activate
    def test_run(self):
        today_timestamp = datetime.datetime.today().timestamp()
        self.harvester.save_attributes(
            {
                'api_url': 'http://test.com',
                'keys_for_list': "x['results']",
                'keys_for_geography_identifier': "x['geom_code']",
                'keys_for_value': "x['value']",
                'keys_for_date': "x['date']",
                'date_format': None
            }
        )
        self.harvester.save_mapping(
            {
                'A': 'A',
                'B': 'B',
                'C': 'C',
            }
        )

        results = {
            'A': {
                'value': 1,
                'date': today_timestamp
            },
            'B': {
                'value': 2,
                'date': today_timestamp
            },
            'C': {
                'value': 1,
                'date': today_timestamp
            }
        }
        responses.add(
            responses.GET,
            f'http://test.com',
            status=200,
            json={
                'results': [{'geom_code': geom_code, 'value': value['value'], 'date': value['date']} for geom_code, value in results.items()]
            }
        )
        self.harvester.run()
        log = self.harvester.harvesterlog_set.last()
        self.assertEqual(log.status, 'Done')
        for indicator_value in self.harvester.indicator.indicatorvalue_set.all():
            self.assertEqual(results[indicator_value.geometry.identifier]['value'], indicator_value.value)
