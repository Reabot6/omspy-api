"""
* Production code from (SFG) | seofg.xyz
* Built by Reabot6 | github.com/reabot6
*
* This file is part of the omspy-api open source release.
* Licensed under the MIT License.
"""
from api.common import constants

N_USERS = 11
N_TENANTS = 5

ADMIN = constants.TENANT_USER_ROLE_TYPE.ADMIN.value
GENERAL = constants.TENANT_USER_ROLE_TYPE.GENERAL.value

TENANT_USERS = {
    1:  (1, 1, ADMIN),
    2:  (1, 2, GENERAL),
    3:  (2, 2, ADMIN),
    4:  (3, 1, GENERAL),
    5:  (3, 3, ADMIN),
    6:  (4, 1, ADMIN),
    7:  (5, 2, GENERAL),
    8:  (6, 3, GENERAL),
    9:  (7, 1, GENERAL),
    10: (8, 2, GENERAL),
    11: (9, 3, GENERAL),
    12: (10, 1, GENERAL),
}
