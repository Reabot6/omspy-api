"""
* Production code from (SFG) | seofg.xyz
* Built by Reabot6 | github.com/reabot6
*
* This file is part of the omspy-api open source release.
* Licensed under the MIT License.
"""
from django.urls import path, re_path

from core.views.index import index


app_name = "core"

urlpatterns = [
    path("", index),
    re_path(r"^.*$", index),
]
