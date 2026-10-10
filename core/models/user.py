"""
* Production code from (SFG) | seofg.xyz
* Built by Reabot6 | github.com/reabot6
*
* This file is part of the omspy-api open source release.
* Licensed under the MIT License.
"""
import os

from django.db import models

from api.common.utils import generate_random_letters
from core.models.base_models import BaseUserModel


def get_user_image_path(instance, filename):
    _, ext = os.path.splitext(filename)
    return f"images/user/{instance.id}/{generate_random_letters(24)}{ext}"


class User(BaseUserModel):
    class Meta(BaseUserModel.Meta):
        db_table = "users"

    disable_promotion = models.BooleanField(default=False)
    email = models.EmailField(max_length=200, unique=True)
    first_name = models.CharField(max_length=200)
    image = models.ImageField(verbose_name="user image", null=True, blank=True, upload_to=get_user_image_path)
    language_code = models.CharField(max_length=20, default="en")
    last_name = models.CharField(max_length=200)
    status = models.IntegerField(default=0)
    timezone_code = models.CharField(max_length=200, default="UTC")

    def __str__(self):
        return f"({self.id}) {self.first_name} {self.last_name} <{self.email}>"
