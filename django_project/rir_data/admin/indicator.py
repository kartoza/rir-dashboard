from django.contrib import admin
from rir_data.models.indicator import (
    Indicator, IndicatorGroup, IndicatorFrequency,
    IndicatorValue, IndicatorExtraValue
)


class IndicatorValueAdmin(admin.ModelAdmin):
    class IndicatorExtraValueRuleInline(admin.TabularInline):
        model = IndicatorExtraValue
        extra = 0

    list_display = ('indicator', 'date', 'geometry', 'value')
    list_filter = ('indicator', 'date', 'geometry')
    search_fields = ('indicator',)
    inlines = (IndicatorExtraValueRuleInline,)


class IndicatorFrequencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'frequency')


class IndicatorAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'group', 'frequency', 'show_in_traffic_light',
        'geometry_reporting_level',)
    list_editable = ('show_in_traffic_light',)
    list_filter = ('group', 'show_in_traffic_light')


admin.site.register(IndicatorGroup, admin.ModelAdmin)
admin.site.register(IndicatorFrequency, IndicatorFrequencyAdmin)
admin.site.register(IndicatorValue, IndicatorValueAdmin)
admin.site.register(Indicator, IndicatorAdmin)
