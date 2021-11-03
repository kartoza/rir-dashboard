from django.shortcuts import reverse
from ._base import AdminView


class GeographyView(AdminView):
    template_name = 'dashboard/admin/geography/view.html'

    @property
    def dashboard_title(self):
        return 'Management: Geography View'

    @property
    def context_view(self) -> dict:
        """
        Return context for specific view by instance
        """
        context = {
            'levels': self.instance.geometry_levels_in_order,
            'url': reverse(
                'geometry-geojson-api', args=[
                    self.instance.slug, 'level', 'date'
                ]
            )
        }
        return context
