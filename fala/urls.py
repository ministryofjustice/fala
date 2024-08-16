# coding=utf-8
from django.conf import settings, Settings

from django.urls import re_path, path
from adviser.views import AccessibilityView, AdviserView, SearchView, PrivacyView
from django.views.generic import TemplateView
from django.views.static import serve

urlpatterns = [
    re_path(r"^accessibility-statement$", AccessibilityView.as_view(), name="accessibility_statement"),
    re_path(r"^privacy$", PrivacyView.as_view(), name="privacy"),
    re_path(r"^$", AdviserView.as_view(), name="adviser"),
    re_path(r"^search$", SearchView.as_view(), name="search"),
    path(
        "robots.txt",
        TemplateView.as_view(template_name=Settings.ROBOTS_TXT, content_type="text/plain"),
    ),
] + [re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT})]
