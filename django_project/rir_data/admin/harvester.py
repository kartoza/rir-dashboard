from django import forms
from django.contrib import admin
from django.utils.html import mark_safe
from django.shortcuts import reverse
from rir_data.models.harvester import (
    Harvester, HarvesterAttribute, HarvesterLog
)

POPULATION_TRACKING_TOOL = 'rir_data.harvester.ipc.PopulationTrackingTool'
HARVESTERS = (
    (POPULATION_TRACKING_TOOL, POPULATION_TRACKING_TOOL),
)


class HarvesterAttributeInline(admin.TabularInline):
    model = HarvesterAttribute
    fields = ('value',)
    readonly_fields = ('name',)
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False


class HarvesterLogInline(admin.TabularInline):
    model = HarvesterLog
    readonly_fields = ('harvester', 'start_time', 'end_time', 'status', 'note')
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False


class HarvesterForm(forms.ModelForm):
    harvester_class = forms.ChoiceField(choices=HARVESTERS)

    class Meta:
        model = Harvester
        fields = '__all__'


def harvest_data(modeladmin, request, queryset):
    for harvester in queryset:
        harvester.run()


harvest_data.short_description = 'Harvest data'


class HarvesterAdmin(admin.ModelAdmin):
    form = HarvesterForm
    inlines = [HarvesterAttributeInline, HarvesterLogInline]
    list_display = ('id', '_indicator', 'harvester_class', 'active', 'is_finished',)
    list_editable = ('active',)
    actions = (harvest_data,)
    search_fields = ('indicator__name',)

    def _indicator(self, object: Harvester):
        return mark_safe(f'<a href="{reverse("admin:rir_data_indicator_change", args=[object.pk])}">{object.indicator.__str__()}</a>')

    def is_finished(self, object: Harvester):
        if not object.is_run:
            return mark_safe('<img src="/static/admin/img/icon-yes.svg" alt="True">')
        else:
            return mark_safe('<img src="/static/admin/img/icon-no.svg" alt="True">')


admin.site.register(Harvester, HarvesterAdmin)
