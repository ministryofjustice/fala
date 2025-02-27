# coding=utf-8
from django.conf import settings
from django.urls import resolve, reverse
from django.views.generic import TemplateView
from fala.common.base_form_components import AdviserRootForm
from fala.common.mixin_for_views import CommonContextMixin, TranslationMixin


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
