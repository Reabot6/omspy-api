"""
* Production code from (SFG) | seofg.xyz
* Built by Reabot6 | github.com/reabot6
*
* This file is part of the omspy-api open source release.
* Licensed under the MIT License.
"""
from .constants import N_TENANTS
from .test_data_command import TestDataCommand
from core import models


class Command(TestDataCommand):
    def insert_data(self):
        for i in range(1, N_TENANTS + 1):
            tenant = models.Tenant(name=f"Tenant{str(i).zfill(3)}")
            tenant.set_domain()
            tenant.save()
