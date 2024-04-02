from .base import *  # noqa: F401,F403
import os

DEBUG = True
ALLOWED_HOSTS = ["localhost"]
DEBUG_STATIC = True
LAALAA_API_HOST = os.environ.get(
    "LAALAA_API_HOST", "https://laa-legal-adviser-api-staging.apps.live-1.cloud-platform.service.justice.gov.uk"
)
ENVIRONMENT = "dev"
FEATURE_FLAG_NO_MAP = False
