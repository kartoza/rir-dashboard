from core.settings.utils import ABS_PATH
from rir_harvester.models.harvester import ExcelHarvester
from rir_harvester.tests.model_factories import HarvesterF
from rir_harvester.tests.test_harvesters._base import BaseHarvesterTest


class APIWithGeograpyAndDate(BaseHarvesterTest):
    """ Test for Harvester : APIWithGeograpyAndDate """

    def test_no_attr_error(self):
        harvester = HarvesterF(
            indicator=self.indicator,
            harvester_class=ExcelHarvester[0]
        )
        harvester.run()
        log = harvester.harvesterlog_set.last()
        self.assertEqual(log.status, 'Error')
        self.assertEqual(
            log.note, 'file is required and it is empty'
        )

    def test_run(self):
        filepath = ABS_PATH('rir_harvester', 'tests', 'test_harvesters', 'fixtures', 'excel_harvester_test.xlsx')
        harvester = HarvesterF(
            harvester_class=ExcelHarvester[0]
        )
        harvester.save_default_attributes(instance=self.instance)
        harvester.save_attributes(
            {
                'date': '2010-01-01',
                'sheet_name': 'Sheet 1',
                'column_name_administration_code': 'geom_code',
                'instance_slug': self.instance.slug,
                'file': filepath,
                self.indicator.name: 'Indicator 1'

            }
        )
        harvester.run()
        log = harvester.harvesterlog_set.last()
        self.assertEqual(log.status, 'Done')
        self.assertEqual(
            self.indicator.indicatorvalue_set.get(
                geometry__identifier='A').value, 3
        )
        self.assertEqual(
            self.indicator.indicatorvalue_set.get(
                geometry__identifier='A').date.strftime("%Y-%m-%d"), '2010-01-01'
        )
        self.assertEqual(
            self.indicator.indicatorvalue_set.get(
                geometry__identifier='B').value, 2
        )
        self.assertEqual(
            self.indicator.indicatorvalue_set.get(
                geometry__identifier='B').date.strftime("%Y-%m-%d"), '2010-01-01'
        )
        self.assertEqual(
            self.indicator.indicatorvalue_set.get(
                geometry__identifier='C').value, 1
        )
        self.assertEqual(
            self.indicator.indicatorvalue_set.get(
                geometry__identifier='C').date.strftime("%Y-%m-%d"), '2010-01-01'
        )
