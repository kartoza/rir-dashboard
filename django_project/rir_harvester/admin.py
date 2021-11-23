from django.contrib import admin
from django.shortcuts import reverse
from django.utils.html import mark_safe
from rir_harvester.models import (
    Harvester, HarvesterAttribute, HarvesterMappingValue, HarvesterLog
)


class HarvesterAttributeInline(admin.TabularInline):
    model = HarvesterAttribute
    fields = ('value',)
    readonly_fields = ('name',)
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False


class HarvesterMappingValueInline(admin.TabularInline):
    model = HarvesterMappingValue
    fields = ('remote_value', 'platform_value')
    extra = 1


class HarvesterLogInline(admin.TabularInline):
    model = HarvesterLog
    readonly_fields = ('harvester', 'start_time', 'end_time', 'status', 'note')
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False


def harvest_data(modeladmin, request, queryset):
    for harvester in queryset:
        harvester.run()


harvest_data.short_description = 'Harvest data'


class HarvesterAdmin(admin.ModelAdmin):
    actions = (harvest_data,)
    inlines = [HarvesterAttributeInline, HarvesterMappingValueInline, HarvesterLogInline]
    list_display = ('id', '_indicator', 'harvester_class', 'active', 'is_finished',)
    list_editable = ('active',)
    search_fields = ('indicator__name',)

    def _indicator(self, object: Harvester):
        return mark_safe(
            f'<a href="{reverse("admin:rir_data_indicator_change", args=[object.pk])}">{object.indicator.__str__()}</a>'
        )

    def is_finished(self, object: Harvester):
        if not object.is_run:
            return mark_safe('<img src="/static/admin/img/icon-yes.svg" alt="True">')
        else:
            return mark_safe('<img src="/static/admin/img/icon-no.svg" alt="True">')


admin.site.register(Harvester, HarvesterAdmin)
