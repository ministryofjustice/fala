# coding=utf-8
from django.conf import settings
from django.urls import resolve, reverse
from django.views.generic import TemplateView
from fala.common.base_form_components import AdviserRootForm
from fala.common.mixin_for_views import CommonContextMixin, TranslationMixin
from django.http import HttpResponseRedirect
from django.utils.translation import activate


class AdviserSearchView(CommonContextMixin, TranslationMixin, TemplateView):
    template_name = "adviser/search.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = AdviserRootForm(data=request.GET or None)
        view_name = resolve(request.path_info).url_name
        current_url = reverse(view_name)

        context.update(
            {
                "form": form,
                "data": {},
                "errorList": [],
                "current_url": current_url,
                "CHECK_LEGAL_AID_URL": settings.CHECK_LEGAL_AID_URL,
                "translation_link": self.translation_link(request),
                "language": self.language(request),
            }
        )

        return self.render_to_response(context)


def set_language(request):
    if request.method == "POST":
        lang_code = request.POST.get("language", "en")
        next_url = request.POST.get("next", "/")

        response = HttpResponseRedirect(next_url)
        response.set_cookie("django_language", lang_code, max_age=30 * 24 * 60 * 60)  # Set cookie for 30 days

        activate(lang_code)  # Change the language immediately
        return response
