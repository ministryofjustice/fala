from django.conf import settings


def ga_id(request):
    return {"GA_ID": settings.GA_ID}
