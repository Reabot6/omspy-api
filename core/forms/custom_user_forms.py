"""
* Production code from (SFG) | seofg.xyz
* Built by Reabot6 | github.com/reabot6
*
* This file is part of the omspy-api open source release.
* Licensed under the MIT License.
"""
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from core import models


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = models.User
        fields = ("first_name", "last_name", "email", "status", "language_code", "timezone_code")
        field_classes = None


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = models.User
        fields = ("first_name", "last_name", "email", "image", "status", "language_code", "timezone_code")
        field_classes = None
