import factory
from rir_data.models.instance import Instance


class InstanceF(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Instance {}'.format(n))

    class Meta:
        model = Instance
