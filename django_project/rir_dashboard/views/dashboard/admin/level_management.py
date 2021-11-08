from django.shortcuts import get_object_or_404, redirect, reverse
from ._base import AdminView
from rir_data.models.geometry import GeometryLevelName, GeometryLevelInstance
from rir_data.models.instance import Instance


class GeographyLevelManagementView(AdminView):
    template_name = 'dashboard/admin/geography/level-management.html'

    @property
    def dashboard_title(self):
        return 'Level Management'

    @property
    def context_view(self) -> dict:
        """
        Return context for specific view by instance
        """
        context = {
            'instance_levels': self.instance.geometry_levels_in_order,
            'levels': GeometryLevelName.objects.all()
        }
        return context

    def post(self, request, **kwargs):
        self.instance = get_object_or_404(
            Instance, slug=kwargs.get('slug', '')
        )
        levels = request.POST.get('level', None)
        if levels:
            levels = levels.split(',')
            self.instance.geometry_levels.delete()

            prev = None
            for level in levels:
                GeometryLevelInstance.objects.get_or_create(
                    instance=self.instance,
                    level_id=level,
                    parent_id=prev
                )
                prev = level
        return redirect(
            reverse(
                'geography-level-management-view', args=[self.instance.slug]
            )
        )
