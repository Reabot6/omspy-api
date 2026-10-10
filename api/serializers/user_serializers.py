"""
* Production code from (SFG) | seofg.xyz
* Built by Reabot6 | github.com/reabot6
*
* This file is part of the omspy-api open source release.
* Licensed under the MIT License.
"""
import logging

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.common import exceptions, utils
from api.serializers.base_serializers import BaseModelSerializer
from core import models


logger = logging.getLogger(__name__)


class NewUserSerializer(BaseModelSerializer):
    invitation_code = serializers.CharField(required=False, write_only=True)
    verification_code = serializers.CharField(required=False, write_only=True)

    class Meta(BaseModelSerializer.Meta):
        model = models.User
        read_only_fields = ("status",) + BaseModelSerializer.Meta.read_only_fields
        extra_kwargs = {
            **BaseModelSerializer.Meta.extra_kwargs,
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        validated_data = self._stamp_create(validated_data)
        if "invitation_code" not in validated_data and "verification_code" not in validated_data:
            raise ValidationError("An invitation code or verification code is required.")
        validated_data.pop("invitation_code", None)
        validated_data.pop("verification_code", None)
        user = models.User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validate(self, data):
        if "invitation_code" in data:
            invite = models.TenantInvitationCode.objects.get(email=data["email"], invitation_code=data["invitation_code"])
            if utils.get_utc_now() > invite.valid_until:
                raise exceptions.TenantInvitationCodeExpired()

        if "verification_code" in data:
            code = models.EmailVerificationCode.objects.get(email=data["email"], verification_code=data["verification_code"])
            if utils.get_utc_now() > code.valid_until:
                raise exceptions.EmailVerificationCodeExpired()

        return self.set_blank_explicitly(data, fields=["groups", "user_permissions"])


class UserSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = models.User
        read_only_fields = ("status",) + BaseModelSerializer.Meta.read_only_fields
        exclude = ("password",) + BaseModelSerializer.Meta.exclude

    def create(self, validated_data):
        validated_data = self._stamp_create(validated_data)
        user = models.User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
            instance.save()
        return instance


class UserPasswordSerializer(BaseModelSerializer):
    password = serializers.CharField(max_length=200, min_length=8)
    new_password = serializers.CharField(required=False, max_length=200, min_length=8)

    class Meta:
        model = models.User
        exclude = None
        fields = ("password", "new_password")

    def update(self, instance, validated_data):
        instance = super().update(instance, {"password": validated_data["new_password"]})
        instance.set_password(validated_data["new_password"])
        instance.save()
        return instance

    def validate(self, data):
        user = models.User.objects.get(pk=self.user.id)
        if not user.check_password(data["password"]):
            raise ValidationError("Current password is incorrect.")
        if data["password"] == data["new_password"]:
            raise ValidationError("New password must differ from the current password.")
        return data
