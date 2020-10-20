from django.conf import settings


def ga_id(request):
    return {"GA_ID": settings.GA_ID}


def current_environment(request):
    return {"ENVIRONMENT": settings.ENVIRONMENT}
