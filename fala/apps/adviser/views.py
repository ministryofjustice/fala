# coding=utf-8
from django.conf import settings
from django.http import HttpResponse
from django.template import loader
from django.urls import resolve, reverse
from django.views.generic import TemplateView

from .forms import AdviserSearchForm, RegionNotFoundException, Region
from .laa_laa_paginator import LaaLaaPaginator


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

REGION_TO_LINK = {
    Region.NI: {
        "link": "https://www.nidirect.gov.uk/articles/legal-aid-schemes",
        "region": "Northern Ireland",
    },
    Region.IOM:  {
        "link": "https://www.gov.im/categories/benefits-and-financial-support/legal-aid/",
        "region": "Isle of Man",
    },
    Region.JERSEY: {
        "link": "https://www.legalaid.je/",
        "region": "Jersey",
    },
    Region.GUERNSEY: {
        "link": "https://www.gov.gg/legalaid",
        "region": "Guernsey",
    },
    Region.SCOTLAND: {
        "link": "https://www.mygov.scot/legal-aid/",
        "region": "Scotland",
    },
}

def fala_search(request):
    form = AdviserSearchForm(data=request.GET or None)

    if settings.FEATURE_FLAG_NO_MAP:
        try:
            data = form.search()
            if data:
                pages = LaaLaaPaginator(data["count"], 10, 3, form.current_page)
                params = {
                "postcode": form.cleaned_data["postcode"],
                "name": form.cleaned_data["name"],
            }
            categories = list(map(lambda c: "categories=" + c, form.cleaned_data["categories"]))
            context = {"form": form, "data": data, "pages": pages, "params": params, "categories": categories}
                template = loader.get_template("adviser/results.html")
            else:
                template = loader.get_template("adviser/search.html")
                context = {
                    "form": form
                }
            return HttpResponse(template.render(context, request))

        except RegionNotFoundException as cde:
            data = REGION_TO_LINK[cde.region]
            context = {
                "postcode": form.cleaned_data["postcode"],
                "link": data["link"],
                "region": data["region"]
            }
            template = loader.get_template("adviser/other_region.html")
            return HttpResponse(template.render(context, request))
    else:
        data = form.search()
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
