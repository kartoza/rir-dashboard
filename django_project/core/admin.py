from django.contrib import admin
from core.models import GeometryLevel, Geometry


class GeometryAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'name', 'alias', 'geometry_level', 'child_of')
    list_filter = ('geometry_level', 'child_of')


class GeometryLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'lower_of')


admin.site.register(GeometryLevel, GeometryLevelAdmin)
admin.site.register(Geometry, GeometryAdmin)
