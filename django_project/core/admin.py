from django import forms
from django.contrib import admin
from django.utils.html import mark_safe
from django.shortcuts import reverse
from core.models import GeometryLevel, Geometry


class GeometryAdmin(admin.ModelAdmin):
    list_display = ('name', 'identifier', 'geometry_level', 'child_of')
    list_filter = ('geometry_level', 'child_of')


class GeometryLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'lower_of')


admin.site.register(GeometryLevel, GeometryLevelAdmin)
admin.site.register(Geometry, GeometryAdmin)
