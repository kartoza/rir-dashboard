from core.models.preferences import SitePreferences
from core.serializer.site_preferences import SitePreferencesSerializer


def global_context(request):
    pref = SitePreferences.preferences()
    return SitePreferencesSerializer(pref).data
