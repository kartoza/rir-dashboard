from django.test.testcases import TestCase
from core.tests.model_factories import SitePreferencesF


class SitePreferencesTest(TestCase):
    """ Test for SitePreferences model """

    def setUp(self):
        self.site_title = 'Test Site'

    def test_create_site_preference(self):
        preference = SitePreferencesF(
            site_title=self.site_title
        )
        self.assertEquals(preference.site_title, self.site_title)
