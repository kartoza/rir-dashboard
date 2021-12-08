from django.contrib import admin
from rir_data.models.basemap_layer import (
    BasemapLayer, BasemapLayerParameter
)


class BasemapLayerParameterInline(admin.TabularInline):
    model = BasemapLayerParameter
    extra = 0


class BasemapLayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'icon', 'show_on_map', 'enable_by_default')
    inlines = (BasemapLayerParameterInline,)
    list_editable = ('show_on_map', 'enable_by_default')


admin.site.register(BasemapLayer, BasemapLayerAdmin)
