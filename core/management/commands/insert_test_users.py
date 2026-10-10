"""
* Production code from (SFG) | seofg.xyz
* Built by Reabot6 | github.com/reabot6
*
* This file is part of the omspy-api open source release.
* Licensed under the MIT License.
"""
from .constants import N_USERS
from .test_data_command import TestDataCommand
from core import models


class Command(TestDataCommand):
    def insert_data(self):
        for i in range(1, N_USERS + 1):
            user = models.User(
                first_name=f"F{str(i).zfill(3)}",
                last_name=f"L{str(i).zfill(3)}",
                email=f"test{str(i).zfill(3)}@test.com",
            )
            user.set_password("testtest")
            user.save()
