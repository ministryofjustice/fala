# coding=utf-8
from django.conf import settings
from django.http import HttpResponse
from django.template import loader
from django.urls import resolve, reverse
from django.views.generic import TemplateView

from .forms import AdviserSearchForm
from .laa_laa_paginator import LaalaaPaginator

# This is only used for the root(/) url - form now points to /search
# regardless of feature flag being on or off
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
                "GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY,
                "LAALAA_API_HOST": settings.LAALAA_API_HOST,
            }
        )

        return self.render_to_response(context)


class AccessibilityView(TemplateView):
    template_name = "adviser/accessibility-statement.html"

def fala_search(request):
    form = AdviserSearchForm(data=request.GET or None)
    data = form.search()
    if settings.FEATURE_FLAG_NO_MAP:
        template = loader.get_template("adviser/results.html")
        pages = LaalaaPaginator(data, 10, 3, form.current_page)
        context = {
            "form": form,
            "data": data,
            "pages": pages
        }
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template("adviser/search.html")
        view_name = resolve(request.path_info).url_name
        current_url = reverse(view_name)
        context = {
                    "form": form,
                    "data": data,
                    "current_url": current_url,
                    "GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY,
        }
        return HttpResponse(template.render(context, request))
