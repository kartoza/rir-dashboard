from django.contrib import admin
from rir_data.models.link import Link


class LinkAdmin(admin.ModelAdmin):
    list_display = ('url', 'name', 'instance', 'is_public', 'order', 'instance')
    list_filter = ('instance',)
    list_editable = ('order', 'is_public')


admin.site.register(Link, LinkAdmin)
