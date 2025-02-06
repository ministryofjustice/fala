# coding=utf-8
from django.conf import settings
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from fala.common.mixin_for_views import CommonContextMixin, TranslationMixin


class SetLanguageView(CommonContextMixin, TranslationMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context.update(
            {
                "translation_link": self.translation_link(request, *args, **kwargs),
            }
        )
        return_link = request.GET.get("return_link", "/")

        response = HttpResponseRedirect(return_link, context)
        language_code = request.GET.get("language_code", False)

        if language_code is not False:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language_code)

        return response
