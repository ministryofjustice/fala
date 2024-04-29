# coding=utf-8
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path, path, include
from adviser.views import AccessibilityView, AdviserView, SearchView
from django.views.static import serve

urlpatterns = [
    re_path(r"^accessibility-statement$", AccessibilityView.as_view(), name="accessibility_statement"),
    re_path(r"^$", AdviserView.as_view(), name="adviser"),
    re_path(r"^search$", SearchView.as_view(), name="search"),
    path("", include("django_prometheus.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG_STATIC:
    urlpatterns += [re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT})]
