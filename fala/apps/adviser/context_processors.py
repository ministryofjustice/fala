from django.conf import settings


def current_environment(request):
    return {"ENVIRONMENT": settings.ENVIRONMENT}
