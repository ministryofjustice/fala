# coding=utf-8
from fala.common.mixin_for_views import CommonContextMixin, TranslationMixin
from django.views.generic import TemplateView
from django.utils.http import url_has_allowed_host_and_scheme


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

    def get(self, request, **kwargs):
        response = super().get(request, **kwargs)

        context = response.context_data

        referer = request.META.get("HTTP_REFERER", "/")
        host = request.get_host()
        previous_url = referer if url_has_allowed_host_and_scheme(referer, allowed_hosts={host}) else "/"

        context.update({"previous_url": previous_url})

        return self.render_to_response(context)
