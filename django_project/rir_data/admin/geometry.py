from django.contrib import admin
from rir_data.models.geometry import Geometry, GeometryLevelName, GeometryLevelInstance


class GeometryAdmin(admin.ModelAdmin):
    list_display = (
        'identifier', 'instance', 'name', 'alias',
        'geometry_level', 'child_of', 'active_date_from', 'active_date_to'
    )
    list_filter = ('instance', 'geometry_level', 'child_of')


class GeometryLevelInstanceAdmin(admin.ModelAdmin):
    list_display = ('level', 'instance', 'parent')
    list_filter = ('instance',)


admin.site.register(GeometryLevelName, admin.ModelAdmin)
admin.site.register(GeometryLevelInstance, GeometryLevelInstanceAdmin)
admin.site.register(Geometry, GeometryAdmin)
