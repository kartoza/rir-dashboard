from django.contrib import admin
from rir_data.models.geometry import Geometry, GeometryLevelName, GeometryLevelInstance


class GeometryAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'name', 'alias', 'geometry_level', 'child_of')
    list_filter = ('geometry_level', 'child_of')


class GeometryLevelNameAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')


class GeometryLevelInstanceAdmin(admin.ModelAdmin):
    list_display = ('level', 'instance', 'parent')
    list_filter = ('instance',)


admin.site.register(GeometryLevelName, GeometryLevelNameAdmin)
admin.site.register(GeometryLevelInstance, GeometryLevelInstanceAdmin)
admin.site.register(Geometry, GeometryAdmin)
