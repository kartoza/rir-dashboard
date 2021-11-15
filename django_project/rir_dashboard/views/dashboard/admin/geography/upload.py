from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Polygon
from django.shortcuts import redirect, reverse, render, get_object_or_404
from rir_dashboard.views.dashboard.admin._base import AdminView
from rir_dashboard.forms.geometry import GeometryForm, ADD_JUST_NEW, REPLACE_AND_ADD
from rir_data.models.geometry import Geometry, GeometryUploader, GeometryUploaderLog
from rir_data.models.instance import Instance


class GeographyUploadView(AdminView):
    template_name = 'dashboard/admin/geography/upload.html'

    @property
    def dashboard_title(self):
        return 'Upload Geography'

    @property
    def context_view(self) -> dict:
        """
        Return context for specific view by instance
        """
        context = {
            'instance_levels': self.instance.geometry_levels_in_order,
            'url': reverse(
                'geometry-geojson-api', args=[
                    self.instance.slug, 'level', 'date'
                ]
            ),
            'form': GeometryForm(level=self.instance.geometry_levels_in_order)
        }
        return context

    def post(self, request, **kwargs):
        self.instance = get_object_or_404(
            Instance, slug=kwargs.get('slug', '')
        )
        form = GeometryForm(request.POST, request.FILES, level=self.instance.geometry_levels_in_order)
        if form.is_valid():
            geojson = form.cleaned_data['geojson']
            instance_geometries = self.instance.geometries()
            geometries = instance_geometries.filter(
                geometry_level=form.cleaned_data['level']
            )
            levels = self.instance.geometry_levels_in_order
            level_idx = levels.index(form.cleaned_data['level'])
            is_most_top_level = level_idx == 0

            # save data
            uploader = GeometryUploader.objects.create(
                file=request.FILES['geojson']
            )
            level = form.cleaned_data['level']
            for feature in geojson['features']:
                try:
                    properties = feature['properties']
                    identifier = properties['identifier']
                    name = properties['name']
                    parent_identifier = properties['parent_identifier']
                    if form.cleaned_data['replace_method'] == ADD_JUST_NEW:
                        try:
                            geometries.get(
                                identifier__iexact=identifier,
                                geometry_level=level
                            )
                            note = 'Geometry exist'
                        except Geometry.DoesNotExist:
                            try:
                                parent = None
                                if not is_most_top_level:
                                    parent = instance_geometries.get(
                                        identifier__iexact=parent_identifier,
                                        geometry_level=levels[level_idx - 1]
                                    )
                                geometry = GEOSGeometry(str(feature['geometry']))
                                if isinstance(geometry, Polygon):
                                    geometry = MultiPolygon(geometry)
                                Geometry.objects.get_or_create(
                                    instance=self.instance,
                                    identifier=identifier,
                                    geometry_level=level,
                                    defaults={
                                        'name': name,
                                        'child_of': parent,
                                        'geometry': GEOSGeometry(geometry)
                                    }
                                )
                                note = 'Geometry created'
                            except Geometry.DoesNotExist:
                                note = f'Parent {parent_identifier} does not found'

                        GeometryUploaderLog.objects.create(
                            uploader=uploader,
                            identifier=identifier,
                            note=note
                        )
                except Exception as e:
                    print(f'{e}')

            return redirect(
                reverse(
                    'geography-management-view', args=[self.instance.slug]
                )
            )
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(
            request,
            self.template_name,
            context
        )
