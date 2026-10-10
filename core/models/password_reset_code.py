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
from core.models.base_models import BaseModel


class PasswordResetCode(BaseModel):
    class Meta(BaseModel.Meta):
        db_table = "password_reset_codes"

    email = models.EmailField(max_length=200)
    reset_code = models.CharField(max_length=200, unique=True)
    valid_until = models.DateTimeField()

    def set_reset_code(self):
        self.reset_code = utils.generate_random_letters(length=settings.PASSWORD_RESET_CODE_LENGTH)
        self.valid_until = utils.get_utc_now() + datetime.timedelta(
            minutes=settings.PASSWORD_RESET_CODE_LIFETIME_MINS
        )

    def __str__(self):
        return f"({self.id}) {self.email}"
