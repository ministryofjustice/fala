import os
from .base import *  # noqa: F401,F403

settings_required = ("SECRET_KEY", "ZENDESK_API_USERNAME", "ZENDESK_API_TOKEN")

for key in settings_required:
    if key not in os.environ:
        raise Exception("'{}' Environment variable is required. please provide".format(key))
