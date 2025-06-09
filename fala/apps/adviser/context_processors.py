import datetime
from django.conf import settings


def current_environment(request):
    return {"ENVIRONMENT": settings.ENVIRONMENT}


def govuk_rebrand(request):
    govuk_rebrand_enabled = datetime.datetime.now() > datetime.datetime(2025, 6, 25)
    if not govuk_rebrand_enabled and settings.ENVIRONMENT != "production":
        govuk_rebrand_enabled = request.GET.get("govuk_rebrand_enabled", "false").lower() == "true"

    return {"GOVUK_REBRAND_ENABLED": govuk_rebrand_enabled}
