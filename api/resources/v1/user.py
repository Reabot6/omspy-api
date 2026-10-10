"""
* Production code from (SFG) | seofg.xyz
* Built by Reabot6 | github.com/reabot6
*
* This file is part of the omspy-api open source release.
* Licensed under the MIT License.
"""
import logging

from django.db import transaction
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api import serializers
from api.resources.decorators import soft_user_data_api, user_data_api
from core import models


logger = logging.getLogger(__name__)


class UserListView(APIView):
    permission_classes = (AllowAny,)

    @transaction.atomic
    def post(self, request):
        serializer = serializers.NewUserSerializer(data=request.data, user=request.user)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        models.EmailVerificationCode.objects.filter(email=user.email).delete()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserView(APIView):
    @soft_user_data_api
    def get(self, request, user_id):
        user = models.User.objects.get(pk=request.user.id if user_id == 0 else user_id)
        return Response(serializers.UserSerializer(user).data, status=status.HTTP_200_OK)

    @user_data_api
    def put(self, request, user_id):
        user = models.User.objects.get(pk=request.user.id)
        serializer = serializers.UserSerializer(user, data=request.data, user=request.user, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @user_data_api
    def delete(self, request, user_id):
        user = models.User.objects.get(pk=request.user.id)
        data = serializers.UserSerializer(user).data
        user.delete()
        return Response(data, status=status.HTTP_200_OK)


class UserPasswordView(APIView):
    @user_data_api
    def put(self, request, user_id):
        user = models.User.objects.get(pk=user_id)
        serializer = serializers.UserPasswordSerializer(user, data=request.data, user=request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserTenantListView(APIView):
    @user_data_api
    def get(self, request, user_id):
        tenant_users = models.TenantUser.objects.filter(user_id=request.user.id)
        tenants = [tu.tenant for tu in tenant_users]
        return Response(serializers.TenantSerializer(tenants, many=True).data, status=status.HTTP_200_OK)
