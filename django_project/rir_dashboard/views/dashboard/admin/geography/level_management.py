import json
from django.shortcuts import get_object_or_404, redirect, reverse
from rir_dashboard.views.dashboard.admin._base import AdminView
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
        level_in_tree = self.instance.geometry_levels_in_tree
        context = {
            'level_in_tree': level_in_tree,
            'levels': GeometryLevelName.objects.all()
        }
        return context

    def post(self, request, **kwargs):
        self.instance = get_object_or_404(
            Instance, slug=kwargs.get('slug', '')
        )
        levels = request.POST.get('level', None)
        if levels:
            levels = json.loads(levels)
            self.instance.geometry_instance_levels.delete()

            self.save_level_tree(None, levels)
        return redirect(
            reverse(
                'geography-level-management-view', args=[self.instance.slug]
            )
        )

    def save_level_tree(self, parent_id, level_data):
        for id, value in level_data.items():
            GeometryLevelInstance.objects.get_or_create(
                instance=self.instance,
                level_id=id,
                parent_id=parent_id
            )
            self.save_level_tree(id, value['child'])
