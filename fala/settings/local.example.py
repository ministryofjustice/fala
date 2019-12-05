from .base import *  # noqa: F401,F403
import os

DEBUG = True
ALLOWED_HOSTS = ["localhost"]
DEBUG_STATIC = True
LAALAA_API_HOST = os.environ.get("LAALAA_API_HOST", "http://0.0.0.0:8001")
