from django.contrib import admin
from scenario.models.scenario import ScenarioLevel


class ScenarioLevelAdmin(admin.ModelAdmin):
    list_display = ('level', 'name')


admin.site.register(ScenarioLevel, ScenarioLevelAdmin)
