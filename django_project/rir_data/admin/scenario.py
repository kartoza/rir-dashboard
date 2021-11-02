from django.contrib import admin
from rir_data.models.scenario import ScenarioLevel


class ScenarioLevelAdmin(admin.ModelAdmin):
    list_display = ('level', 'name', 'instance')
    list_filter = ('instance',)


admin.site.register(ScenarioLevel, ScenarioLevelAdmin)
