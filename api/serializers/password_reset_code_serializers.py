"""
* Production code from (SFG) | seofg.xyz
* Built by Reabot6 | github.com/reabot6
*
* This file is part of the omspy-api open source release.
* Licensed under the MIT License.
"""
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.common import exceptions, utils
from api.serializers.base_serializers import BaseModelSerializer, BaseSerializer
from core import models


class PasswordResetCodeSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = models.PasswordResetCode
        read_only_fields = ("reset_code", "valid_until") + BaseModelSerializer.Meta.read_only_fields

    def create(self, validated_data):
        validated_data = self._stamp_create(validated_data)
        obj = models.PasswordResetCode(**validated_data)
        obj.set_reset_code()
        obj.save()
        return obj

    def validate(self, data):
        if not models.User.objects.filter(email=data["email"]).exists():
            raise exceptions.EmailNotRegistered(f"{data['email']} is not registered.")
        return data


class PasswordResetSerializer(BaseModelSerializer):
    reset_code = serializers.CharField()

    class Meta(BaseModelSerializer.Meta):
        model = models.User
        exclude = None
        fields = ("email", "password", "reset_code")
        extra_kwargs = {
            **BaseModelSerializer.Meta.extra_kwargs,
            "password": {"write_only": True},
        }

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.set_password(validated_data["password"])
        instance.save()
        return instance

    def validate(self, data):
        if not models.User.objects.filter(email=data["email"]).exists():
            raise exceptions.EmailNotRegistered(f"{data['email']} is not registered.")
        query = models.PasswordResetCode.objects.filter(email=data["email"], reset_code=data["reset_code"])
        if not query.exists():
            raise ValidationError("Invalid reset code.")
        if utils.get_utc_now() > query.get().valid_until:
            raise exceptions.PasswordResetCodeExpired()
        return data


class PasswordResetEmailSerializer(BaseSerializer):
    reset_code = serializers.CharField(max_length=settings.PASSWORD_RESET_CODE_LENGTH, write_only=True)
    email = serializers.CharField(max_length=200, required=False)

    def validate(self, data):
        if len(data["reset_code"]) != settings.PASSWORD_RESET_CODE_LENGTH:
            raise serializers.ValidationError("Invalid password reset code.")
        query = models.PasswordResetCode.objects.filter(reset_code=data["reset_code"])
        if query.count() != 1:
            raise serializers.ValidationError("Invalid password reset code.")
        return query.get()
