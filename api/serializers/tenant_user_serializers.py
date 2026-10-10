"""
* Production code from (SFG) | seofg.xyz
* Built by Reabot6 | github.com/reabot6
*
* This file is part of the omspy-api open source release.
* Licensed under the MIT License.
"""
import logging

from rest_framework import serializers

from api.common import exceptions, utils
from api.serializers.base_serializers import BaseModelSerializer
from api.serializers.tenant_serializers import TenantSerializer
from api.serializers.user_serializers import UserSerializer
from core import models


logger = logging.getLogger(__name__)


class TenantUserSerializer(BaseModelSerializer):
    tenant = TenantSerializer(required=False, read_only=True)
    user = UserSerializer(required=False, read_only=True)
    tenant_id = serializers.IntegerField(write_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta(BaseModelSerializer.Meta):
        model = models.TenantUser

    def validate(self, data):
        if self.user.id != data["user_id"]:
            raise serializers.ValidationError("User mismatch.")
        if self.tenant.id != data["tenant_id"]:
            raise serializers.ValidationError("Tenant mismatch.")
        return data


class InvitedTenantUserSerializer(BaseModelSerializer):
    tenant = TenantSerializer(required=False, read_only=True)
    user = UserSerializer(required=False, read_only=True)
    tenant_id = serializers.IntegerField(write_only=True)
    user_id = serializers.IntegerField(write_only=True)
    invitation_code = serializers.CharField(write_only=True)

    class Meta(BaseModelSerializer.Meta):
        model = models.TenantUser

    def create(self, validated_data):
        validated_data.pop("invitation_code")
        return super().create(validated_data)

    def validate(self, data):
        if self.user.id != data["user_id"]:
            raise serializers.ValidationError("User mismatch.")
        invite = models.TenantInvitationCode.objects.get(
            email=self.user.email, invitation_code=data["invitation_code"]
        )
        if invite.tenant_id != data["tenant_id"]:
            raise serializers.ValidationError("Invitation code is not for this tenant.")
        if utils.get_utc_now() > invite.valid_until:
            raise exceptions.TenantInvitationCodeExpired()
        return data
