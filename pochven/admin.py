from django.contrib import admin

from pochven.models import Constellation, SolarSystem


class ConstellationAdmin(admin.ModelAdmin):
    pass


class SolarSystemAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "constellation",
        "claimed_by",
        "home",
        "order",
    ]
    list_filter = [
        "constellation",
    ]
    search_fields = [
        "name",
    ]


admin.site.register(Constellation, ConstellationAdmin)
admin.site.register(SolarSystem, SolarSystemAdmin)
