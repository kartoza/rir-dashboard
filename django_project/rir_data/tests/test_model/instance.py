from django.test.testcases import TestCase
from django.template.defaultfilters import slugify
from rir_data.tests.model_factories import (
    InstanceF, BasemapLayerF,
    ContextLayerF, LinkF
)


class InstanceTest(TestCase):
    """ Test for Instance model """

    def setUp(self):
        self.name = 'Test Instance'

    def test_create_instance(self):
        instance = InstanceF(
            name=self.name
        )
        self.assertEquals(instance.name, self.name)
        self.assertEquals(instance.slug, slugify(self.name))

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
