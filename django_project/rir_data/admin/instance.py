from django.contrib import admin
from rir_data.models.instance import Instance


class InstanceAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'icon')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Instance, InstanceAdmin)
