"""
* Production code from (SFG) | seofg.xyz
* Built by Reabot6 | github.com/reabot6
*
* This file is part of the omspy-api open source release.
* Licensed under the MIT License.
"""
from rest_framework import serializers

from api.serializers.base_serializers import BaseModelSerializer
from core import models


class FailedLoginAttemptSerializer(BaseModelSerializer):
    attempted_at = serializers.DateTimeField(required=False, read_only=True)

    class Meta(BaseModelSerializer.Meta):
        model = models.FailedLoginAttempt
