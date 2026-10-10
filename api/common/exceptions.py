"""
* Production code from (SFG) | seofg.xyz
* Built by Reabot6 | github.com/reabot6
*
* This file is part of the omspy-api open source release.
* Licensed under the MIT License.
"""
from rest_framework.exceptions import APIException


class DataAlreadyRegistered(APIException):
    def __init__(self, detail="Data already registered.", code=None):
        super().__init__(detail=detail, code=code)


class EmailNotRegistered(APIException):
    def __init__(self, detail="Email is not registered.", code=None):
        super().__init__(detail=detail, code=code)


class EmailVerificationCodeExpired(APIException):
    def __init__(self, detail="Verification code has expired.", code=None):
        super().__init__(detail=detail, code=code)


class LoginAttemptLimitError(APIException):
    def __init__(self, detail="Too many failed login attempts. Try again later.", code=None):
        super().__init__(detail=detail, code=code)


class OwnershipError(APIException):
    def __init__(self, detail="You do not have permission to access this resource.", code=None):
        super().__init__(detail=detail, code=code)


class PasswordResetCodeExpired(APIException):
    def __init__(self, detail="Password reset code has expired.", code=None):
        super().__init__(detail=detail, code=code)


class RequestSizeError(APIException):
    def __init__(self, detail="Request payload exceeds the allowed size.", code=None):
        super().__init__(detail=detail, code=code)


class TenantInvitationCodeExpired(APIException):
    def __init__(self, detail="Invitation code has expired.", code=None):
        super().__init__(detail=detail, code=code)
