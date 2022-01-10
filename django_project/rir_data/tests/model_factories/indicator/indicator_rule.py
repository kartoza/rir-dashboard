import factory
from rir_data.models.indicator import IndicatorScenarioRule
from rir_data.tests.model_factories.indicator import IndicatorF
from rir_data.tests.model_factories.scenario import ScenarioLevelF


class IndicatorScenarioRuleF(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Scenario Rule {}'.format(n))
    scenario_level = factory.SubFactory(ScenarioLevelF)
    indicator = factory.SubFactory(IndicatorF)
    color = factory.Sequence(lambda n: '#{}'.format(n))

    class Meta:
        model = IndicatorScenarioRule
