"""
* Production code from (SFG) | seofg.xyz
* Built by Reabot6 | github.com/reabot6
*
* This file is part of the omspy-api open source release.
* Licensed under the MIT License.
"""
from rest_framework import serializers
from rest_framework.fields import empty

from api.common import constants, exceptions


class BaseSerializer(serializers.Serializer):
    def __init__(self, instance=None, data=empty, tenant=None, tenant_user=None, user=None, extra_request=None, **kwargs):
        if extra_request and data is not empty:
            if isinstance(data, list):
                for item in data:
                    item.update(extra_request)
            else:
                data.update(extra_request)
        super().__init__(instance=instance, data=data, **kwargs)
        self.tenant = tenant
        self.tenant_user = tenant_user
        self.user = user


class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ("created_at", "updated_at", "deleted_at")
        read_only_fields = ("id",)
        extra_kwargs = {
            "created_by": {"write_only": True},
            "updated_by": {"write_only": True},
        }

    def __init__(self, instance=None, data=empty, tenant=None, tenant_user=None, user=None, extra_request=None, **kwargs):
        if extra_request and data is not empty:
            if isinstance(data, list):
                for item in data:
                    item.update(extra_request)
            else:
                data.update(extra_request)
        super().__init__(instance=instance, data=data, **kwargs)
        self.tenant = tenant
        self.tenant_user = tenant_user
        self.user = user

    def create(self, validated_data):
        return super().create(self._stamp_create(validated_data))

    def update(self, instance, validated_data):
        return super().update(instance, self._stamp_update(validated_data))

    def _actor(self):
        if self.tenant_user is not None:
            return str(self.tenant_user.user.id)
        if self.user is not None:
            return constants.BUILTIN_USER.ANONYMOUS.value if self.user.id is None else str(self.user.id)
        return constants.BUILTIN_USER.SYSTEM.value

    def _stamp_create(self, data):
        actor = self._actor()
        data["created_by"] = actor
        data["updated_by"] = actor
        return data

    def _stamp_update(self, data):
        data["updated_by"] = self._actor()
        return data

    def fill_missing_fields_by_instance(self, data):
        if self.instance is None:
            return data
        for field in (f.field_name for f in self._writable_fields):
            if field not in data:
                data[field] = self.instance._meta.get_field(field).value_from_object(self.instance)
        return data

    def set_blank_explicitly(self, data, fields):
        for field in fields:
            val = data.get(field)
            if val in (None, "", [], {}):
                data.pop(field, None)
        return data


class DefaultListSerializer(serializers.ListSerializer):
    def validate(self, data):
        if len(data) > 20:
            raise exceptions.RequestSizeError("Batch size must be <= 20.")
        return data


class StringListField(serializers.ListField):
    child = serializers.CharField(max_length=100)
