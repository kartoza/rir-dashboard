from django.contrib import admin
from rir_data.models.program import (
    Program, ProgramIntervention
)


class ProgramInterventionInline(admin.TabularInline):
    model = ProgramIntervention
    extra = 0


class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'instance')
    list_filter = ('instance',)
    inlines = (ProgramInterventionInline,)


admin.site.register(Program, ProgramAdmin)
