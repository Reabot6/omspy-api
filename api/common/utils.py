"""
* Production code from (SFG) | seofg.xyz
* Built by Reabot6 | github.com/reabot6
*
* This file is part of the omspy-api open source release.
* Licensed under the MIT License.
"""
import datetime
import random
import secrets
import string

import pytz


_ALPHABET = string.ascii_letters + string.digits


def generate_random_letters(length: int) -> str:
    return "".join(secrets.choice(_ALPHABET) for _ in range(length))


def get_utc_now() -> datetime.datetime:
    return datetime.datetime.now(tz=pytz.utc)


def to_utc(dt: datetime.datetime) -> datetime.datetime:
    return dt.astimezone(pytz.utc)


def get_far_future_datetime() -> datetime.datetime:
    return to_utc(datetime.datetime(2999, 12, 31, tzinfo=pytz.utc))
