# coding=utf-8
from django.conf import settings
from django.urls import re_path, include
from fala.apps.adviser.views import AdviserSearchView
from fala.apps.category_search.views import CategorySearchView
from fala.common.results_view import ResultsView
from fala.common.footer_views import (
    AccessibilityView,
    PrivacyView,
    CookiesView,
)
from fala.common.compliance_views import (
    RobotsTxtView,
    SecurityTxtView,
)
from django.views.static import serve

urlpatterns = [
    re_path(r"^i18n/", include("django.conf.urls.i18n"), name="set_language"),
    re_path(r"^accessibility-statement$", AccessibilityView.as_view(), name="accessibility_statement"),
    re_path(r"^cookies$", CookiesView.as_view(), name="cookies"),
    re_path(r"^privacy$", PrivacyView.as_view(), name="privacy"),
    re_path(r"^$", AdviserSearchView.as_view(), name="adviser"),
    re_path(r"^search$", ResultsView.as_view(), name="results"),
    re_path(r"^robots\.txt$", RobotsTxtView.as_view(), name="robots_txt"),
    re_path(r"^security\.txt$", SecurityTxtView.as_view(), name="security_txt"),
    re_path(r"^check/(?P<category>[\w-]+)$", CategorySearchView.as_view(), name="category_search"),
    re_path(r"^check$", CategorySearchView.as_view(), name="category_search_query"),
] + [re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT})]
