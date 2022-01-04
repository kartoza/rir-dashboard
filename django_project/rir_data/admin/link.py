from django.contrib import admin
from rir_data.models.link import Link


class LinkAdmin(admin.ModelAdmin):
    list_display = ('url', 'name', 'instance', 'order')
    list_filter = ('instance',)
    list_editable = ('order',)


admin.site.register(Link, LinkAdmin)
