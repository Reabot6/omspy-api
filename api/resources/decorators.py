"""
* Production code from (SFG) | seofg.xyz
* Built by Reabot6 | github.com/reabot6
*
* This file is part of the omspy-api open source release.
* Licensed under the MIT License.
"""
import logging
from functools import partial, wraps

from box import Box
from rest_framework.exceptions import PermissionDenied, ValidationError

from api import serializers
from api.common import constants, exceptions
from core import models


logger = logging.getLogger(__name__)


def _get_tenant(domain):
    try:
        return models.Tenant.objects.get(domain=domain)
    except models.Tenant.DoesNotExist:
        raise ValidationError(f"Tenant with domain '{domain}' not found.")


def _get_tenant_user(request, tenant):
    try:
        return models.TenantUser.objects.get(tenant_id=tenant.id, user_id=request.user.id)
    except models.TenantUser.DoesNotExist:
        raise ValidationError("You are not a member of this tenant.")


def _get_tenant_user_by_id(tenant, tenant_user_id):
    try:
        return models.TenantUser.objects.get(pk=tenant_user_id, tenant_id=tenant.id)
    except models.TenantUser.DoesNotExist:
        raise ValidationError("Tenant user not found.")


def _get_tenant_user_scoped_to_request(request, tenant, tenant_user_id):
    try:
        return models.TenantUser.objects.get(pk=tenant_user_id, tenant_id=tenant.id, user_id=request.user.id)
    except models.TenantUser.DoesNotExist:
        raise ValidationError("Tenant user not found or does not belong to the requesting user.")


def tenant_user_data_api(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request = args[1]
        tenant = _get_tenant(kwargs["domain"])
        _get_tenant_user(request, tenant)
        _get_tenant_user_by_id(tenant, kwargs["tenant_user_id"])
        tenant_user = _get_tenant_user(request, tenant)
        serializer = serializers.TenantUserSerializer(tenant_user)
        return func(*args, Box(serializer.data), **kwargs)
    return wrapper


def self_tenant_user_data_api(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request = args[1]
        tenant = _get_tenant(kwargs["domain"])
        tenant_user = _get_tenant_user_scoped_to_request(request, tenant, kwargs["tenant_user_id"])
        serializer = serializers.TenantUserSerializer(tenant_user)
        return func(*args, Box(serializer.data), **kwargs)
    return wrapper


def tenant_user_api(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request = args[1]
        tenant = _get_tenant(kwargs["domain"])
        tenant_user = _get_tenant_user(request, tenant)
        serializer = serializers.TenantUserSerializer(tenant_user)
        return func(*args, Box(serializer.data), **kwargs)
    return wrapper


def tenant_admin_api(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request = args[1]
        tenant = _get_tenant(kwargs["domain"])
        tenant_user = _get_tenant_user(request, tenant)
        if tenant_user.role_type != constants.TENANT_USER_ROLE_TYPE.ADMIN.value:
            raise PermissionDenied("Only tenant admins can perform this action.")
        serializer = serializers.TenantUserSerializer(tenant_user)
        return func(*args, Box(serializer.data), **kwargs)
    return wrapper


def tenant_api(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        tenant = _get_tenant(kwargs["domain"])
        serializer = serializers.TenantSerializer(tenant)
        return func(*args, Box(serializer.data), **kwargs)
    return wrapper


def _user_data_api(func, allow_zero_id: bool):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request = args[1]
        user_id = kwargs.get("user_id")
        if user_id is None:
            raise ValidationError("user_id is missing in endpoint.")
        if user_id == 0:
            if not allow_zero_id:
                raise ValidationError("Invalid user ID.")
        elif user_id != request.user.id:
            raise exceptions.OwnershipError()
        return func(*args, **kwargs)
    return wrapper


soft_user_data_api = partial(_user_data_api, allow_zero_id=True)
user_data_api = partial(_user_data_api, allow_zero_id=False)
