from django.conf import settings


def current_environment(request):
    return {"ENVIRONMENT": settings.ENVIRONMENT}


def feature_flag(request):
    return {"FALA_NO_MAP": settings.FEATURE_FLAG_NO_MAP}
