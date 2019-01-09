# coding=utf-8
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from adviser.views import AdviserView

urlpatterns = [url(r"^$", AdviserView.as_view(), name="adviser")] + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)

if settings.DEBUG_STATIC:
    urlpatterns += [
        url(r"^static/(?P<path>.*)$", "django.views.static.serve", {"document_root": settings.STATIC_ROOT})
    ]
