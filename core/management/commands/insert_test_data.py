"""
* Production code from (SFG) | seofg.xyz
* Built by Reabot6 | github.com/reabot6
*
* This file is part of the omspy-api open source release.
* Licensed under the MIT License.
"""
from django.core.management import call_command

from .test_data_command import TestDataCommand


class Command(TestDataCommand):
    RESOURCES = ["users", "tenants", "tenant_users"]

    def insert_data(self):
        for resource in self.RESOURCES:
            call_command(f"insert_test_{resource}")
