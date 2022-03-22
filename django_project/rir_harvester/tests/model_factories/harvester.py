import factory
from rir_harvester.models.harvester import Harvester
from rir_harvester.models.harvester_attribute import HarvesterAttribute, HarvesterMappingValue
from rir_data.tests.model_factories.indicator import IndicatorF


class HarvesterF(factory.django.DjangoModelFactory):
    indicator = factory.SubFactory(IndicatorF)

    class Meta:
        model = Harvester


class HarvesterAttributeF(factory.django.DjangoModelFactory):
    harvester = factory.SubFactory(HarvesterF)

    class Meta:
        model = HarvesterAttribute


class HarvesterMappingValueF(factory.django.DjangoModelFactory):
    harvester = factory.SubFactory(HarvesterF)

    class Meta:
        model = HarvesterMappingValue
