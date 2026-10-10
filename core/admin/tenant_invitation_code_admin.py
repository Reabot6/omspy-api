"""
* Production code from (SFG) | seofg.xyz
* Built by Reabot6 | github.com/reabot6
*
* This file is part of the omspy-api open source release.
* Licensed under the MIT License.
"""
from django.contrib import admin

from core import models


class TenantInvitationCodeAdmin(admin.ModelAdmin):
    list_display = ("id", "tenant_user_id", "email", "valid_until")
    list_display_links = list_display
    search_fields = ("id", "email")
    ordering = ("id", "valid_until")

    def save_model(self, request, obj, form, change):
        if not obj.invitation_code:
            obj.set_invitation_code()
        obj.save()
