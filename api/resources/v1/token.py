"""
* Production code from (SFG) | seofg.xyz
* Built by Reabot6 | github.com/reabot6
*
* This file is part of the omspy-api open source release.
* Licensed under the MIT License.
"""
import logging

from ipware import get_client_ip
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api import serializers


logger = logging.getLogger(__name__)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        ip_address, _ = get_client_ip(request)
        data = {**dict(request.data), "ip_address": ip_address}

        class _Request:
            pass

        patched = _Request()
        patched.data = data
        return super().post(patched, *args, **kwargs)


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = serializers.CustomTokenRefreshSerializer


class CustomTokenVerifyView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        return Response({}, status=status.HTTP_200_OK)


class TokenRevokeView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if "refresh" not in request.data:
            raise ValidationError("refresh token is required.")
        token = RefreshToken(request.data["refresh"])
        token.blacklist()
        return Response({"refresh": request.data["refresh"]}, status=status.HTTP_200_OK)
