# coding=utf-8
from fala.common.mixin_for_views import CommonContextMixin, TranslationMixin
from django.views.generic import TemplateView


class FooterView:
    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        context.update(
            {
                "translation_link": self.translation_link(request),
                "language": self.language(request),
            }
        )
        return self.render_to_response(context)


class AccessibilityView(FooterView, CommonContextMixin, TranslationMixin, TemplateView):
    template_name = "adviser/accessibility_statement.html"


class PrivacyView(FooterView, CommonContextMixin, TranslationMixin, TemplateView):
    template_name = "adviser/privacy.html"


class CookiesView(FooterView, CommonContextMixin, TranslationMixin, TemplateView):
    template_name = "adviser/cookies.html"
