# coding=utf-8
from django.conf import settings
from django.urls import resolve, reverse
from django.views.generic import TemplateView, ListView

from .forms import AdviserSearchForm
from .laa_laa_paginator import LaaLaaPaginator
from laalaa.api import PROVIDER_CATEGORIES
from .regions import Region, REGION_TO_LINK


class AdviserView(TemplateView):
    def get_template_names(self) -> list[str]:
        if settings.FEATURE_FLAG_NO_MAP:
            template_name = "adviser/search.html"
        else:
            template_name = "adviser/search_old.html"
        return [template_name]

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
                "FEATURE_FLAG_NO_MAP": settings.FEATURE_FLAG_NO_MAP,
                "CHECK_LEGAL_AID_URL": settings.CHECK_LEGAL_AID_URL,
            }
        )

        return self.render_to_response(context)


class AccessibilityView(TemplateView):
    template_name = "adviser/accessibility-statement.html"


class SearchView(ListView):
    class ErrorState(object):
        def __init__(self, form):
            self._form = form

        @property
        def template_name(self):
            return "search.html"

        def get_queryset(self):
            return []

        def get_context_data(self):
            return {"form": self._form, "data": {}}

    class EnglandOrWalesState(object):
        def __init__(self, form, region):
            self._form = form
            self._data = form.search()
            self._region = region

        @property
        def template_name(self):
            return "results.html"

        def get_queryset(self):
            return self._data.get("results", None)

        def get_context_data(self):
            pages = LaaLaaPaginator(self._data["count"], 10, 3, self._form.current_page)
            params = {
                "postcode": self._form.cleaned_data["postcode"],
                "name": self._form.cleaned_data["name"],
            }
            # create list of tuples which can be passed to urlencode for pagination links
            categories = [("categories", c) for c in self._form.cleaned_data["categories"]]
            region_data = REGION_TO_LINK[self._region]
            return {
                "form": self._form,
                "data": self._data,
                "link": region_data["link"],
                "region": region_data["region"],
                "pages": pages,
                "params": params,
                "FEATURE_FLAG_SURVEY_MONKEY": settings.FEATURE_FLAG_SURVEY_MONKEY,
                "categories": categories,
                "category_selection": self._display_category(),
            }

        def _display_category(self):
            if "categories" in self._form.cleaned_data:
                categories = [PROVIDER_CATEGORIES[cat] for cat in self._form.cleaned_data["categories"]]
                formatted_categories = ", ".join(map(str, categories))

                return formatted_categories
            return []

    class OldMapState(object):
        def __init__(self, form, current_url):
            self.current_url = current_url
            self.form = form

        def get_queryset(self):
            return []

        @property
        def template_name(self):
            return "search_old.html"

        def get_context_data(self):
            return {
                "form": self.form,
                "data": self.form.search(),
                "current_url": self.current_url,
                "GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY,
                "FEATURE_FLAG_NO_MAP": settings.FEATURE_FLAG_NO_MAP,
                "CHECK_LEGAL_AID_URL": settings.CHECK_LEGAL_AID_URL,
            }

    class OtherJurisdictionState(object):

        def __init__(self, region, postcode):
            self._region = region
            self._postcode = postcode

        def get_queryset(self):
            return []

        @property
        def template_name(self):
            return "other_region.html"

        def get_context_data(self):
            region_data = REGION_TO_LINK[self._region]
            return {
                "postcode": self._postcode,
                "link": region_data["link"],
                "region": region_data["region"],
            }

    def get(self, request, *args, **kwargs):
        form = AdviserSearchForm(data=request.GET or None)
        if settings.FEATURE_FLAG_NO_MAP:
            if form.is_valid():
                region = form.region
                if region == Region.ENGLAND_OR_WALES or region == Region.SCOTLAND:
                    self.state = self.EnglandOrWalesState(form, region)
                else:
                    self.state = self.OtherJurisdictionState(region, form.cleaned_data["postcode"])
            else:
                self.state = self.ErrorState(form)
        else:
            view_name = resolve(request.path_info).url_name
            current_url = reverse(view_name)
            self.state = self.OldMapState(form, current_url)
        return super().get(self, request, *args, **kwargs)

    def get_template_names(self):
        return ["adviser/" + self.state.template_name]

    def get_queryset(self):
        return self.state.get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(self.state.get_context_data())
        return context
