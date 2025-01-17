# coding=utf-8
from django.conf import settings
from django.urls import resolve, reverse
from django.views.generic import TemplateView
from .forms import AdviserRootForm
from fala.common.mixin_for_views import CommonContextMixin
from fala.common.utils import POSTCODE_LABEL, POSTCODE_HINT, ORG_LABEL, ORG_HINT, LEGAL_HINT, SEARCH_LABEL


class AdviserSearchView(CommonContextMixin, TemplateView):
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
                "POSTCODE_LABEL": POSTCODE_LABEL,
                "POSTCODE_HINT": POSTCODE_HINT,
                "ORG_LABEL": ORG_LABEL,
                "ORG_HINT": ORG_HINT,
                "LEGAL_HINT": LEGAL_HINT,
                "SEARCH_LABEL": SEARCH_LABEL,
            }
        )

        return self.render_to_response(context)
