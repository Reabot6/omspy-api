"""
* Production code from (SFG) | seofg.xyz
* Built by Reabot6 | github.com/reabot6
*
* This file is part of the omspy-api open source release.
* Licensed under the MIT License.
"""
from .constants import TENANT_USERS
from .test_data_command import TestDataCommand
from core import models


class Command(TestDataCommand):
    def insert_data(self):
        for _, (user_id, tenant_id, role_type) in TENANT_USERS.items():
            models.TenantUser(user_id=user_id, tenant_id=tenant_id, role_type=role_type).save()
