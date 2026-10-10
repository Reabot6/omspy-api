"""
* Production code from (SFG) | seofg.xyz
* Built by Reabot6 | github.com/reabot6
*
* This file is part of the omspy-api open source release.
* Licensed under the MIT License.
"""
from django.db import models

from core.models.base_models import BaseModel


class EmailChange(BaseModel):
    class Meta(BaseModel.Meta):
        db_table = "email_changes"

    user = models.ForeignKey("User", null=False, blank=False, on_delete=models.CASCADE)
    new_email = models.EmailField(max_length=200)
    verification_code = models.CharField(max_length=200, unique=True)
    valid_until = models.DateTimeField()

    def __str__(self):
        return f"({self.id}) {self.user.email} -> {self.new_email}"
