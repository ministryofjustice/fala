# coding=utf-8
from django.conf import settings
from django.core.urlresolvers import resolve, reverse
from django.views.generic import TemplateView

from .forms import AdviserSearchForm


class AdviserView(TemplateView):
    template_name = "adviser/search.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = AdviserSearchForm(data=request.GET or None)
        view_name = resolve(request.path_info).url_name
        current_url = reverse(view_name)

        context.update(
            {
                "form": form,
                "data": form.search(),
                "current_url": current_url,
                "GA_ID": settings.GA_ID,
                "LAALAA_API_HOST": settings.LAALAA_API_HOST,
            }
        )

        return self.render_to_response(context)
