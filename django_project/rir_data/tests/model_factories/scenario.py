import factory
from rir_data.models.scenario import ScenarioLevel
from rir_data.tests.model_factories.instance import InstanceF


class ScenarioLevelF(factory.django.DjangoModelFactory):
    instance = factory.SubFactory(InstanceF)
    name = factory.Sequence(lambda n: 'Scenario Level {}'.format(n))
    level = factory.Sequence(lambda n: n)

    class Meta:
        model = ScenarioLevel
