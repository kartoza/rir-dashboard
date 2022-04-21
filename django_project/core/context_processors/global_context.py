from core.models.preferences import SitePreferences
from core.serializer.site_preferences import SitePreferencesSerializer
from rir_data.models import Instance, Link


def global_context(request):
    pref = SitePreferences.preferences()
    try:
        path = request.path.strip('/').split('/')
        links = Instance.objects.get(slug=path[0]).links
    except (IndexError, ValueError, Instance.DoesNotExist):
        links = Link.objects.filter(instance__isnull=True)
    return {
        'preferences': SitePreferencesSerializer(pref).data,
        'links': links
    }
