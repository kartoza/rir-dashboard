from django.contrib import admin
from rir_data.models.context_layer import (
    ContextLayerGroup, ContextLayer, ContextLayerParameter
)


class ContextLayerParameterInline(admin.TabularInline):
    model = ContextLayerParameter
    extra = 0


class ContextLayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'group', 'show_on_map', 'enable_by_default', 'order')
    inlines = (ContextLayerParameterInline,)
    list_editable = ('show_on_map', 'enable_by_default', 'order')


class ContextLayerGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)


admin.site.register(ContextLayerGroup, ContextLayerGroupAdmin)
admin.site.register(ContextLayer, ContextLayerAdmin)
