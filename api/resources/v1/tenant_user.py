"""
* Production code from (SFG) | seofg.xyz
* Built by Reabot6 | github.com/reabot6
*
* This file is part of the omspy-api open source release.
* Licensed under the MIT License.
"""
import logging

from django.contrib.postgres.search import TrigramSimilarity
from django.db import transaction
from django.db.models import Q, Value
from django.db.models.functions import Concat, Greatest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from api import serializers
from api.common import constants
from api.resources.decorators import self_tenant_user_data_api, tenant_api, tenant_user_api
from core import models


logger = logging.getLogger(__name__)

_SIMILARITY_THRESHOLD = 0.3


class TenantUserListView(APIView):
    @tenant_user_api
    def get(self, request, tenant_user, domain):
        query = models.TenantUser.objects.filter(tenant_id=tenant_user.tenant.id)
        search = request.query_params.get("search", "").strip()
        if search:
            query = self._apply_search(search, query)
        page = self.paginate_queryset(query, request)
        return Response(
            {"results": serializers.TenantUserSerializer(page, many=True).data, "count": self.page.paginator.count},
            status=status.HTTP_200_OK,
        )

    @tenant_api
    @transaction.atomic
    def post(self, request, tenant, domain):
        serializer = serializers.InvitedTenantUserSerializer(
            data=request.data,
            tenant=tenant,
            user=request.user,
            extra_request={"tenant_id": tenant.id},
        )
        serializer.is_valid(raise_exception=True)
        tenant_user = serializer.save()
        models.TenantInvitationCode.objects.filter(email=tenant_user.user.email).delete()
        return Response(serializers.TenantUserSerializer(tenant_user).data, status=status.HTTP_201_CREATED)

    def _apply_search(self, search, query):
        if " " in search:
            return (
                query
                .annotate(username=Concat("user__first_name", Value(" "), "user__last_name"))
                .annotate(name_similarity=TrigramSimilarity("username", search))
                .filter(Q(name_similarity__gt=_SIMILARITY_THRESHOLD) | Q(user__email__icontains=search))
                .order_by("-name_similarity")
            )
        return (
            query
            .annotate(fn_sim=TrigramSimilarity("user__first_name", search))
            .annotate(ln_sim=TrigramSimilarity("user__last_name", search))
            .annotate(name_similarity=Greatest("fn_sim", "ln_sim"))
            .filter(Q(name_similarity__gt=_SIMILARITY_THRESHOLD) | Q(user__email__icontains=search))
            .order_by("-name_similarity")
        )


class TenantUserView(APIView):
    @tenant_user_api
    def get(self, request, tenant_user, domain, tenant_user_id):
        condition = Q(tenant_id=tenant_user.tenant.id) & (
            Q(id=tenant_user_id) if tenant_user_id != 0 else Q(user_id=request.user.id)
        )
        obj = models.TenantUser.objects.get(condition)
        return Response(serializers.TenantUserSerializer(obj).data, status=status.HTTP_200_OK)

    @self_tenant_user_data_api
    def put(self, request, tenant_user, domain, tenant_user_id):
        obj = models.TenantUser.objects.get(pk=tenant_user_id)
        serializer = serializers.TenantUserSerializer(obj, data=request.data, user=obj.user, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @self_tenant_user_data_api
    def delete(self, request, tenant_user, domain, tenant_user_id):
        remaining_admins = (
            models.TenantUser.objects
            .filter(tenant_id=tenant_user.tenant.id, role_type=constants.TENANT_USER_ROLE_TYPE.ADMIN.value)
            .exclude(pk=tenant_user_id)
        )
        if remaining_admins.count() == 0:
            raise RuntimeError("Cannot remove the last admin of a tenant. Assign another admin first.")

        obj = models.TenantUser.objects.get(pk=tenant_user_id, tenant_id=tenant_user.tenant.id)
        data = serializers.TenantUserSerializer(obj).data
        obj.delete()
        return Response(data, status=status.HTTP_200_OK)
