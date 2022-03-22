from django.test.testcases import TestCase
from django.template.defaultfilters import slugify
from rir_data.tests.model_factories import (
    InstanceF, BasemapLayerF,
    ContextLayerF, LinkF, ScenarioLevelF,
    GeometryF, GeometryLevelNameF, GeometryLevelInstanceF,
    IndicatorF, IndicatorValueF, IndicatorGroupF, IndicatorScenarioRuleF
)
from rir_data.models.indicator.indicator import AggregationMethod


class InstanceTest(TestCase):
    """ Test for Instance model """

    def setUp(self):
        self.name = 'Test Instance'

    def test_create(self):
        instance = InstanceF(
            name=self.name
        )
        self.assertEquals(instance.name, self.name)
        self.assertEquals(instance.slug, slugify(self.name))

    def test_scenario_levels(self):
        """
        Test for ScenarioLevel of the instance
        """
        instance_1 = InstanceF()

        # create ScenarioLevel for each instance
        ScenarioLevelF(name='Scenario Level 1', instance=instance_1)
        ScenarioLevelF(name='Scenario Level 2', instance=instance_1)
        ScenarioLevelF(name='Scenario Level 3', instance=instance_1)

        self.assertEquals(instance_1.scenario_levels.count(), 3)
        self.assertEquals(instance_1.scenario_levels[0].name, 'Scenario Level 1')
        self.assertEquals(instance_1.scenario_levels[1].name, 'Scenario Level 2')
        self.assertEquals(instance_1.scenario_levels[2].name, 'Scenario Level 3')

    def test_basemap_layers(self):
        """
        Test for basemaps of the instance
        """
        instance_1 = InstanceF()
        instance_2 = InstanceF()

        # create BasemapLayer for global
        BasemapLayerF(name='Basemap Global', instance=None)

        # create BasemapLayer for each instance
        BasemapLayerF(name='Basemap Instance 1', instance=instance_1)
        BasemapLayerF(name='Basemap Instance 2 1', instance=instance_2, show_on_map=False)
        BasemapLayerF(name='Basemap Instance 2 2', instance=instance_2)

        self.assertEquals(instance_1.basemap_layers.count(), 2)
        self.assertEquals(instance_1.basemap_layers[0].name, 'Basemap Global')
        self.assertEquals(instance_1.basemap_layers[1].name, 'Basemap Instance 1')

        self.assertEquals(instance_2.basemap_layers.count(), 2)
        self.assertEquals(instance_2.basemap_layers[0].name, 'Basemap Global')
        self.assertEquals(instance_2.basemap_layers[1].name, 'Basemap Instance 2 2')

    def test_context_layers(self):
        """
        Test for context of the instance
        """
        instance_1 = InstanceF()
        instance_2 = InstanceF()

        # create ContextLayer for global
        ContextLayerF(name='Context Global', instance=None)

        # create ContextLayer for each instance
        ContextLayerF(name='Context Instance 1', instance=instance_1)
        ContextLayerF(name='Context Instance 2 1', instance=instance_2, show_on_map=False)
        ContextLayerF(name='Context Instance 2 2', instance=instance_2)

        self.assertEquals(instance_1.context_layers.count(), 2)
        self.assertEquals(instance_1.context_layers[0].name, 'Context Global')
        self.assertEquals(instance_1.context_layers[1].name, 'Context Instance 1')

        self.assertEquals(instance_2.context_layers.count(), 2)
        self.assertEquals(instance_2.context_layers[0].name, 'Context Global')
        self.assertEquals(instance_2.context_layers[1].name, 'Context Instance 2 2')

    def test_links(self):
        """
        Test for links of the instance
        """
        instance_1 = InstanceF()
        instance_2 = InstanceF()

        # create Link for global
        LinkF(name='Link Global', instance=None)

        # create Link for each instance
        LinkF(name='Link Instance 1', instance=instance_1)
        LinkF(name='Link Instance 2 1', instance=instance_2)
        LinkF(name='Link Instance 2 2', instance=instance_2)

        self.assertEquals(instance_1.links.count(), 2)
        self.assertEquals(instance_1.links[0].name, 'Link Global')
        self.assertEquals(instance_1.links[1].name, 'Link Instance 1')

        self.assertEquals(instance_2.links.count(), 3)
        self.assertEquals(instance_2.links[0].name, 'Link Global')
        self.assertEquals(instance_2.links[1].name, 'Link Instance 2 1')
        self.assertEquals(instance_2.links[2].name, 'Link Instance 2 2')

    def test_geometries(self):
        """
        Test for geometries of the instance
        """
        instance = InstanceF(
            name=self.name
        )
        country_2 = GeometryLevelNameF()  # make it as not used
        province_2_1 = GeometryLevelNameF()  # make it as not used

        country_1 = GeometryLevelNameF()
        province_1_1 = GeometryLevelNameF()
        province_1_2 = GeometryLevelNameF()
        district_1_1_1 = GeometryLevelNameF()
        district_1_1_2 = GeometryLevelNameF()
        district_1_1_3 = GeometryLevelNameF()
        district_1_2_1 = GeometryLevelNameF()
        district_1_2_2 = GeometryLevelNameF()

        # make it for the instance
        GeometryLevelInstanceF(
            instance=instance, level=country_1, parent=None)
        GeometryLevelInstanceF(
            instance=instance, level=province_1_1, parent=country_1)
        GeometryLevelInstanceF(
            instance=instance, level=province_1_2, parent=country_1)
        GeometryLevelInstanceF(
            instance=instance, level=district_1_1_1, parent=province_1_1)
        GeometryLevelInstanceF(
            instance=instance, level=district_1_1_2, parent=province_1_1)
        GeometryLevelInstanceF(
            instance=instance, level=district_1_1_3, parent=province_1_1)
        GeometryLevelInstanceF(
            instance=instance, level=district_1_2_1, parent=province_1_2)
        GeometryLevelInstanceF(
            instance=instance, level=district_1_2_2, parent=province_1_2)

        self.assertEquals(len(instance.geometry_levels), 8)
        self.assertEquals(instance.geometry_instance_levels.count(), 8)
        self.assertEquals(instance.geometry_levels_in_order, [
            country_1, province_1_1, district_1_1_1, district_1_1_2, district_1_1_3,
            province_1_2, district_1_2_1, district_1_2_2
        ])

    def test_indicators(self):
        instance = InstanceF()
        group_1 = IndicatorGroupF(
            instance=instance
        )
        group_2 = IndicatorGroupF(
            instance=instance
        )
        level_1 = ScenarioLevelF(name='Level 1', level=1)
        level_2 = ScenarioLevelF(name='Level 2', level=2)
        level_3 = ScenarioLevelF(name='Level 3', level=3)
        level_4 = ScenarioLevelF(name='Level 4', level=4)
        country = GeometryLevelNameF(name='country')
        province = GeometryLevelNameF(name='province')
        geom_country = GeometryF(
            instance=instance,
            name='Country', geometry_level=country)
        geom_province_1 = GeometryF(
            instance=instance, name='Province 1',
            geometry_level=province, child_of=geom_country)
        geom_province_2 = GeometryF(
            instance=instance, name='Province 2',
            geometry_level=province, child_of=geom_country)
        geom_province_3 = GeometryF(
            instance=instance, name='Province 3',
            geometry_level=province, child_of=geom_country)

        # level instance init
        GeometryLevelInstanceF(
            instance=instance,
            level=country
        )
        GeometryLevelInstanceF(
            instance=instance,
            level=province,
            parent=country
        )
        # ------------------------------------------------
        # indicator 1
        # ------------------------------------------------
        indicator_1 = IndicatorF(
            name='Name 1',
            group=group_1,
            geometry_reporting_level=province,
            aggregation_method=AggregationMethod.MAJORITY
        )
        rules = [
            IndicatorScenarioRuleF(
                indicator=indicator_1, rule='x==1', scenario_level=level_1
            ),
            IndicatorScenarioRuleF(
                indicator=indicator_1, rule='x==2 or x==3', scenario_level=level_2
            ),
            IndicatorScenarioRuleF(
                indicator=indicator_1, rule='x>=4 and x<=5', scenario_level=level_3
            ),
            IndicatorScenarioRuleF(
                indicator=indicator_1, rule='x>5', scenario_level=level_4
            )
        ]
        # set value
        IndicatorValueF(
            indicator=indicator_1, value=1,
            geometry=geom_province_1
        )
        IndicatorValueF(
            indicator=indicator_1, value=1,
            geometry=geom_province_2
        )
        IndicatorValueF(
            indicator=indicator_1, value=2,
            geometry=geom_province_3
        )
        # ------------------------------------------------
        # indicator 2
        # ------------------------------------------------
        indicator_2 = IndicatorF(
            name='Name 2',
            group=group_1,
            geometry_reporting_level=province,
            aggregation_method=AggregationMethod.MAJORITY
        )
        rules = [
            IndicatorScenarioRuleF(
                indicator=indicator_2, rule='x==1', scenario_level=level_1
            ),
            IndicatorScenarioRuleF(
                indicator=indicator_2, rule='x==2 or x==3', scenario_level=level_2
            ),
            IndicatorScenarioRuleF(
                indicator=indicator_2, rule='x>=4 and x<=5', scenario_level=level_3
            ),
            IndicatorScenarioRuleF(
                indicator=indicator_2, rule='x>5', scenario_level=level_4
            )
        ]
        # set value
        IndicatorValueF(
            indicator=indicator_2, value=3,
            geometry=geom_province_1
        )
        IndicatorValueF(
            indicator=indicator_2, value=2,
            geometry=geom_province_2
        )
        IndicatorValueF(
            indicator=indicator_2, value=2,
            geometry=geom_province_3
        )

        # ------------------------------------------------
        # indicator 3
        # ------------------------------------------------
        indicator_3 = IndicatorF(
            name='Name 3',
            group=group_2,
            geometry_reporting_level=province,
            aggregation_method=AggregationMethod.MAJORITY
        )
        rules = [
            IndicatorScenarioRuleF(
                indicator=indicator_3, rule='x==1', scenario_level=level_1
            ),
            IndicatorScenarioRuleF(
                indicator=indicator_3, rule='x==2 or x==3', scenario_level=level_2
            ),
            IndicatorScenarioRuleF(
                indicator=indicator_3, rule='x>=4 and x<=5', scenario_level=level_3
            ),
            IndicatorScenarioRuleF(
                indicator=indicator_3, rule='x>5', scenario_level=level_4
            )
        ]
        # set value
        IndicatorValueF(
            indicator=indicator_3, value=3,
            geometry=geom_province_1
        )
        IndicatorValueF(
            indicator=indicator_3, value=2,
            geometry=geom_province_2
        )
        IndicatorValueF(
            indicator=indicator_3, value=2,
            geometry=geom_province_3
        )

        indicators, overall_scenario = instance.get_indicators_and_overall_scenario()
        self.assertEquals(overall_scenario, 2)
        indicators_group_1 = indicators[group_1.name]
        self.assertEquals(indicators_group_1['overall_scenario'], 1)
        indicators_group_2 = indicators[group_2.name]
        self.assertEquals(indicators_group_2['overall_scenario'], 2)
