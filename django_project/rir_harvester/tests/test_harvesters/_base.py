from django.test.testcases import TestCase
from rir_data.tests.model_factories import IndicatorF, InstanceF, IndicatorGroupF, GeometryLevelNameF, GeometryF


class BaseHarvesterTest(TestCase):
    """ Base for test API """

    def setUp(self):
        self.instance = InstanceF()
        level = GeometryLevelNameF()
        self.indicator = IndicatorF(
            group=IndicatorGroupF(
                instance=self.instance
            ),
            geometry_reporting_level=level
        )

        GeometryF(
            identifier='A',
            instance=self.instance,
            geometry_level=level
        )

        GeometryF(
            identifier='B',
            instance=self.instance,
            geometry_level=level
        )

        GeometryF(
            identifier='C',
            instance=self.instance,
            geometry_level=level
        )
