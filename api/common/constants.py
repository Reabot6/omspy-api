"""
* Production code from (SFG) | seofg.xyz
* Built by Reabot6 | github.com/reabot6
*
* This file is part of the omspy-api open source release.
* Licensed under the MIT License.
"""
from enum import Enum


class BUILTIN_USER(Enum):
    SYSTEM = "system"
    ANONYMOUS = "anonymous"


class TENANT_USER_ROLE_TYPE(Enum):
    GENERAL = 0
    ADMIN = 100


SEARCH_USER_SIMILARITY_THRESHOLD = 0.8
