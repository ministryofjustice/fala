import os
from .base import *  # noqa: F401,F403

settings_required = (
    "SECRET_KEY",
    "GOOGLE_MAPS_API_KEY",
    "LAALAA_API_HOST",
)

for key in settings_required:
    if key not in os.environ:
        raise Exception("'{}' Environment variable is required. please provide".format(key))
