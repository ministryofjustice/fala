# coding=utf-8
from django.conf import settings
from django.urls import resolve, reverse
from django.views.generic import TemplateView, ListView

from .forms import AdviserSearchForm
from .laa_laa_paginator import LaaLaaPaginator


# https://docs.djangoproject.com/en/5.0/topics/class-based-views - documentation on Class-based views
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
    def get(self, request, *args, **kwargs):
        self._form = AdviserSearchForm(data=request.GET or None)
        self._data = self._form.search()
        return super().get(self, request, *args, **kwargs)

    # Errors from LaaLaaAPI manifest as _data being falsey, so we bounce back to search page
    def get_template_names(self):
        if self._data:
            template = "adviser/results.html"
        else:
            template = "adviser/search.html"
        return [template]

    def get_queryset(self):
        return self._data.get("results", None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"form": self._form, "data": self._data})
        # Only paginate on success. _data is already paginated, so we need our own paginator
        # that can answer questions about next and previous buttons etc.
        if self._data:
            pages = LaaLaaPaginator(self._data["count"], 10, 3, self._form.current_page)
            params = {
                "postcode": self._form.cleaned_data["postcode"],
                "name": self._form.cleaned_data["name"],
            }
            # create list of tuples which can be passed to urlencode for pagnation links
            categories = [("categories", c) for c in self._form.cleaned_data["categories"]]

            context.update({"pages": pages, "params": params, "categories": categories})
        return context
