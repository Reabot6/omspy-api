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
from django.core.mail import send_mass_mail
from django.db import transaction
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from api import serializers
from api.resources.decorators import tenant_admin_api, tenant_user_api
from core import models


logger = logging.getLogger(__name__)

_INVITE_BASE_URL = os.path.join(settings.APP_DOMAIN, "auth/invite/")


class TenantInvitationCodeListView(APIView, api_settings.DEFAULT_PAGINATION_CLASS):
    @tenant_admin_api
    def get(self, request, tenant_user, domain):
        query = models.TenantInvitationCode.objects.filter(tenant_id=tenant_user.tenant.id)
        page = self.paginate_queryset(query, request)
        data = serializers.TenantInvitationCodeSerializer(page, many=True).data
        return Response({"results": data, "count": self.page.paginator.count}, status=status.HTTP_200_OK)

    @tenant_admin_api
    @transaction.atomic
    def post(self, request, tenant_user, domain):
        serializer = serializers.TenantInvitationCodeSerializer(
            data=request.data,
            tenant_user=tenant_user,
            many=isinstance(request.data, list),
            extra_request={"tenant_id": tenant_user.tenant.id},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self._send_invitations(tenant=tenant_user.tenant, sender=tenant_user, data=serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def _send_invitations(self, tenant, sender, data):
        emails = [d["email"] for d in data]
        codes = [d["invitation_code"] for d in data]
        emails, codes = self._exclude_existing_members(tenant.id, emails, codes)
        messages = tuple(self._build_email(tenant, sender, e, c) for e, c in zip(emails, codes))
        send_mass_mail(messages, fail_silently=False)

    def _build_email(self, tenant, sender, email, code):
        url = _INVITE_BASE_URL.rstrip("/") + f"/{code}"
        subject = f"{sender.user.first_name} invited you to {tenant.name} on {settings.APP_NAME}"
        body = (
            f"{sender.user.first_name} {sender.user.last_name} ({sender.user.email}) "
            f"has invited {email} to join {tenant.name}.\n\nAccept: {url}\n\n"
            f"This link expires in {settings.TENANT_INVITATION_CODE_LIFETIME_MINS} minutes."
        )
        return (subject, body, settings.EMAIL_HOST_USER, [email])

    def _exclude_existing_members(self, tenant_id, emails, codes):
        filtered = [
            (e, c) for e, c in zip(emails, codes)
            if not models.TenantUser.objects.filter(tenant_id=tenant_id, user__email=e).exists()
        ]
        if not filtered:
            return [], []
        return zip(*filtered)


class TenantInvitationCodeView(APIView):
    @tenant_admin_api
    def delete(self, request, tenant_user, domain, invitation_code_id):
        obj = models.TenantInvitationCode.objects.get(pk=invitation_code_id, tenant_id=tenant_user.tenant.id)
        query = models.TenantInvitationCode.objects.filter(tenant_id=tenant_user.tenant.id, email=obj.email)
        data = serializers.TenantInvitationCodeSerializer(query, many=True).data
        query.delete()
        return Response(data, status=status.HTTP_200_OK)


class InvitedTenantView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = serializers.InvitedTenantSerializer(data=request.data, user=request.user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
