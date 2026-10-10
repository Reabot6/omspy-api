"""
* Production code from (SFG) | seofg.xyz
* Built by Reabot6 | github.com/reabot6
*
* This file is part of the omspy-api open source release.
* Licensed under the MIT License.
"""
from django.contrib import admin

from core import models
from core.admin import admins


admin.site.register(models.EmailVerificationCode, admins.EmailVerificationCodeAdmin)
admin.site.register(models.PasswordResetCode, admins.PasswordResetCodeAdmin)
admin.site.register(models.User, admins.CustomUserAdmin)
admin.site.register(models.Tenant, admins.TenantAdmin)
admin.site.register(models.TenantInvitationCode, admins.TenantInvitationCodeAdmin)
admin.site.register(models.TenantUser, admins.TenantUserAdmin)
