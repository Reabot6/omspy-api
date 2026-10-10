"""
* Production code from (SFG) | seofg.xyz
* Built by Reabot6 | github.com/reabot6
*
* This file is part of the omspy-api open source release.
* Licensed under the MIT License.
"""
import logging
import os

from django.conf import settings
from django.core.mail import EmailMessage
from django.db import transaction
from ipware import get_client_ip
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api import serializers
from core import models


logger = logging.getLogger(__name__)

_RESET_BASE_URL = os.path.join(settings.APP_DOMAIN, "auth/password/reset/")


class PasswordResetCodeView(APIView):
    permission_classes = (AllowAny,)

    @transaction.atomic
    def post(self, request):
        serializer = serializers.PasswordResetCodeSerializer(data=request.data, user=request.user)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        self._send_reset_email(obj.email, obj.reset_code)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def _send_reset_email(self, email, code):
        url = _RESET_BASE_URL.rstrip("/") + f"/{code}"
        body = (
            f"You requested a password reset for your {settings.APP_NAME} account.\n\n"
            f"Reset your password here: {url}\n\n"
            f"This link expires in {settings.PASSWORD_RESET_CODE_LIFETIME_MINS} minutes."
        )
        EmailMessage(subject="Reset your password", body=body, to=[email]).send()


class PasswordResetView(APIView):
    permission_classes = (AllowAny,)

    @transaction.atomic
    def post(self, request):
        user = models.User.objects.get(email=request.data["email"])
        serializer = serializers.PasswordResetSerializer(user, data=request.data, user=request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        models.PasswordResetCode.objects.filter(email=user.email).delete()

        ip_address, _ = get_client_ip(request)
        if ip_address:
            models.FailedLoginAttempt.objects.filter(email=user.email, ip_address=ip_address).delete()

        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordResetEmailView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = serializers.PasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
