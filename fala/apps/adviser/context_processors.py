from django.conf import settings


def current_environment(request):
    return {"ENVIRONMENT": settings.ENVIRONMENT}

def govuk_rebrand(request):
    return {"GOVUK_REBRAND_ENABLED": settings.GOVUK_REBRAND_ENABLED}
