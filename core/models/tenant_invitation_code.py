"""
* Production code from (SFG) | seofg.xyz
* Built by Reabot6 | github.com/reabot6
*
* This file is part of the omspy-api open source release.
* Licensed under the MIT License.
"""
import datetime

from django.conf import settings
from django.db import models

from api.common import utils
from core.models.base_models import BaseTenantModel


class TenantInvitationCode(BaseTenantModel):
    class Meta(BaseTenantModel.Meta):
        db_table = "tenant_invitation_codes"

    tenant_user = models.ForeignKey("TenantUser", null=False, blank=False, on_delete=models.CASCADE)
    email = models.EmailField(max_length=200)
    invitation_code = models.CharField(max_length=200, unique=True)
    invited_at = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField()

    def set_invitation_code(self):
        self.invitation_code = utils.generate_random_letters(length=settings.TENANT_INVITATION_CODE_LENGTH)
        self.valid_until = utils.get_utc_now() + datetime.timedelta(
            minutes=settings.TENANT_INVITATION_CODE_LIFETIME_MINS
        )

    def __str__(self):
        return f"({self.id}) {self.email} -> {self.tenant.name}"
