from django.test.testcases import TestCase
from rir_data.tests.model_factories import LinkF


class LinkTest(TestCase):
    """ Test for Link model """

    def setUp(self):
        self.name = 'Link1'

    def test_create_link(self):
        link = LinkF(
            name=self.name
        )
        self.assertEquals(link.name, self.name)
