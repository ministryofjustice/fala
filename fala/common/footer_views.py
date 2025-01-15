# coding=utf-8
from fala.common.mixin_for_views import CommonContextMixin
from django.views.generic import TemplateView


class AccessibilityView(CommonContextMixin, TemplateView):
    template_name = "adviser/accessibility_statement.html"


class PrivacyView(CommonContextMixin, TemplateView):
    template_name = "adviser/privacy.html"


class CookiesView(CommonContextMixin, TemplateView):
    template_name = "adviser/cookies.html"
