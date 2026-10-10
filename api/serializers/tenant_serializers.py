"""
* Production code from (SFG) | seofg.xyz
* Built by Reabot6 | github.com/reabot6
*
* This file is part of the omspy-api open source release.
* Licensed under the MIT License.
"""
from django.conf import settings
from rest_framework import serializers

from api.common import utils
from api.serializers.base_serializers import BaseModelSerializer
from core import models


class TenantSerializer(BaseModelSerializer):
    tenant_user_count = serializers.SerializerMethodField()

    class Meta(BaseModelSerializer.Meta):
        model = models.Tenant
        read_only_fields = ("domain",) + BaseModelSerializer.Meta.read_only_fields

    def get_tenant_user_count(self, obj):
        try:
            return models.TenantUser.objects.filter(tenant_id=obj.id).count()
        except Exception:
            return 0

    def create(self, validated_data):
        validated_data["domain"] = utils.generate_random_letters(length=settings.TENANT_DOMAIN_LENGTH)
        return super().create(validated_data)
