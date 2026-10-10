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
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api import serializers


logger = logging.getLogger(__name__)

_VERIFY_BASE_URL = os.path.join(settings.APP_DOMAIN, "auth/signup/")


class EmailVerificationCodeView(APIView):
    permission_classes = (AllowAny,)

    @transaction.atomic
    def post(self, request):
        serializer = serializers.EmailVerificationCodeSerializer(data=request.data, user=request.user)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        self._send_verification_email(obj.email, obj.verification_code)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def _send_verification_email(self, email, code):
        url = _VERIFY_BASE_URL.rstrip("/") + f"/{code}"
        body = (
            f"Thanks for signing up to {settings.APP_NAME}.\n\n"
            f"Confirm your email here: {url}\n\n"
            f"This link expires in {settings.EMAIL_VERIFICATION_CODE_LIFETIME_MINS} minutes. "
            f"If you did not sign up, you can ignore this email."
        )
        EmailMessage(subject="Confirm your email address", body=body, to=[email]).send()


class VerifiedEmailView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = serializers.VerifiedEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
