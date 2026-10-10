"""
* Production code from (SFG) | seofg.xyz
* Built by Reabot6 | github.com/reabot6
*
* This file is part of the omspy-api open source release.
* Licensed under the MIT License.
"""
from django.contrib import admin

from core import models


class TenantUserAdmin(admin.ModelAdmin):
    list_display = ("id", "tenant_id", "user_id", "role_type")
    list_display_links = list_display
    search_fields = ("id",)
    ordering = ("id", "tenant_id", "user_id")
