import urllib.parse
from django.test.testcases import TestCase
from rir_data.tests.model_factories import (
    ContextLayerF, ContextLayerParameterF, ContextLayerStyleF
)
from rir_data.serializer.context_layer import ContextLayerSerializer


class BasemapLayerTest(TestCase):
    """ Test for Basemap model """

    def setUp(self):
        self.name = 'Context Layer 1'
        self.params = {
            'param 1': 'value 1',
            'param 2': 'value 2',
            'param 3': 'value 3',
        }
        self.style = {
            'style 1': 'value 1',
            'style 2': 'value 2',
            'style 3': 'value 3',
        }

    def test_create(self):
        context_layer = ContextLayerF(
            name=self.name
        )

        for name, value in self.params.items():
            ContextLayerParameterF(
                context_layer=context_layer,
                name=name,
                value=value
            )
        for name, value in self.style.items():
            ContextLayerStyleF(
                context_layer=context_layer,
                name=name,
                value=value
            )

        context_layer_data = ContextLayerSerializer(context_layer).data
        self.assertEquals(context_layer_data['name'], self.name)
        for key, value in context_layer_data['parameters'].items():
            self.assertEquals(urllib.parse.quote(self.params[key]), value)
        for key, value in context_layer_data['style'].items():
            self.assertEquals(self.style[key], value)
