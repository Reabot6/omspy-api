"""
* Production code from (SFG) | seofg.xyz
* Built by Reabot6 | github.com/reabot6
*
* This file is part of the omspy-api open source release.
* Licensed under the MIT License.
"""
import logging

import django.core.exceptions as django_exc
import rest_framework as drf
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import exception_handler

from api.common import exceptions


logger = logging.getLogger(__name__)

_EXC_STATUS_MAP = [
    (Http404,                            status.HTTP_404_NOT_FOUND),
    (django_exc.PermissionDenied,        status.HTTP_403_FORBIDDEN),
    (drf.exceptions.NotFound,            status.HTTP_404_NOT_FOUND),
    (drf.exceptions.PermissionDenied,    status.HTTP_403_FORBIDDEN),
    (drf.exceptions.ValidationError,     status.HTTP_400_BAD_REQUEST),
    (drf.exceptions.NotAuthenticated,    status.HTTP_401_UNAUTHORIZED),
    (exceptions.DataAlreadyRegistered,   status.HTTP_409_CONFLICT),
    (exceptions.EmailNotRegistered,      status.HTTP_400_BAD_REQUEST),
    (exceptions.EmailVerificationCodeExpired, status.HTTP_403_FORBIDDEN),
    (exceptions.OwnershipError,          status.HTTP_403_FORBIDDEN),
    (exceptions.PasswordResetCodeExpired, status.HTTP_403_FORBIDDEN),
    (exceptions.RequestSizeError,        status.HTTP_413_REQUEST_ENTITY_TOO_LARGE),
    (exceptions.TenantInvitationCodeExpired, status.HTTP_403_FORBIDDEN),
]


def _status_for(exc) -> int:
    for exc_type, status_code in _EXC_STATUS_MAP:
        if isinstance(exc, exc_type):
            return status_code
    return status.HTTP_500_INTERNAL_SERVER_ERROR


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    logger.error("%s: %s", type(exc).__name__, exc)

    status_code = _status_for(exc)
    payload = {
        "type": type(exc).__name__,
        "action": str(context.get("view", "")),
        "messages": [],
        "status": status_code,
        "error": True,
    }

    if response is None or not isinstance(response, Response):
        payload["messages"] = [str(exc)]
        return Response(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if isinstance(exc.detail, dict):
        for key, value in exc.detail.items():
            if key == api_settings.NON_FIELD_ERRORS_KEY:
                payload["messages"].append(" ".join(str(v) for v in value))
            else:
                payload["messages"].append(f"{key}: {' '.join(str(v) for v in value)}")
    elif isinstance(exc.detail, list):
        payload["messages"] = [str(d) for d in exc.detail]
    else:
        payload["messages"] = [str(exc.detail)]

    return Response(payload, status=status_code)
