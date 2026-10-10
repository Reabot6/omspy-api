"""
* Production code from (SFG) | seofg.xyz
* Built by Reabot6 | github.com/reabot6
*
* This file is part of the omspy-api open source release.
* Licensed under the MIT License.
"""
from django.db import models

from core.models.base_models import BaseModel


class FailedLoginAttempt(BaseModel):
    class Meta(BaseModel.Meta):
        db_table = "failed_login_attempts"

    ip_address = models.CharField(max_length=200, blank=True, default="")
    email = models.EmailField(max_length=200)
    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"({self.id}) {self.email} from {self.ip_address}"
