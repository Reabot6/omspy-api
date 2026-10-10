"""
* Production code from (SFG) | seofg.xyz
* Built by Reabot6 | github.com/reabot6
*
* This file is part of the omspy-api open source release.
* Licensed under the MIT License.
"""
import datetime
import logging

from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from api.common import exceptions, utils
from api.serializers.failed_login_attempt_serializers import FailedLoginAttemptSerializer
from core import models


logger = logging.getLogger(__name__)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = models.User.EMAIL_FIELD
    ip_address = serializers.CharField(allow_null=True, required=False)

    @classmethod
    def get_token(cls, user):
        return super().get_token(user)

    def validate(self, data):
        login_locked = self._is_login_locked(data)

        try:
            tokens = super().validate(data)
        except AuthenticationFailed:
            self._record_failed_attempt(data)
            if login_locked:
                raise exceptions.LoginAttemptLimitError()
            raise

        if login_locked:
            raise exceptions.LoginAttemptLimitError()

        tokens["access_expires_in"] = int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds())
        tokens["refresh_expires_in"] = int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds())
        return tokens

    def _record_failed_attempt(self, data):
        serializer = FailedLoginAttemptSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def _is_login_locked(self, data) -> bool:
        now = utils.get_utc_now()
        since = now - datetime.timedelta(minutes=settings.LOGIN_LOCK_PERIOD_MINS)
        query = models.FailedLoginAttempt.objects.filter(
            email=data["email"], attempted_at__range=[since, now]
        )
        if data.get("ip_address"):
            query = query.filter(ip_address=data["ip_address"])
        return query.count() >= settings.FAILED_LOGIN_ATTEMPT_MAX_COUNT


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, data):
        data = super().validate(data)
        data["access_expires_in"] = int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds())
        return data
