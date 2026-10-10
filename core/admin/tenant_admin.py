"""
* Production code from (SFG) | seofg.xyz
* Built by Reabot6 | github.com/reabot6
*
* This file is part of the omspy-api open source release.
* Licensed under the MIT License.
"""
from django.contrib import admin

from core import models


class TenantAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "domain", "description")
    list_display_links = list_display
    search_fields = ("id", "name")
    ordering = ("id", "name")

    def save_model(self, request, obj, form, change):
        if not obj.domain:
            obj.set_domain()
        obj.save()
