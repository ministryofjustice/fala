# coding=utf-8
import urllib

from django.conf import settings
from django.urls import resolve, reverse
from django.views.generic import TemplateView, ListView

from .forms import AdviserSearchForm, AdviserRootForm
from .laa_laa_paginator import LaaLaaPaginator
from .regions import Region


class CommonContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            {
                # this is so that `govuk_frontend_jinja/template.html` can be extended and without CSP complaining
                "cspNonce": getattr(self.request, "csp_nonce", None),
                # this is added in so that an additional class is added the <body>
                "bodyClasses": f"fala-{settings.ENVIRONMENT}",
            }
        )
        return context


class AdviserView(CommonContextMixin, TemplateView):
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
            }
        )

        return self.render_to_response(context)


class AccessibilityView(CommonContextMixin, TemplateView):
    template_name = "adviser/accessibility_statement.html"


class PrivacyView(CommonContextMixin, TemplateView):
    template_name = "adviser/privacy.html"


class CookiesView(CommonContextMixin, TemplateView):
    template_name = "adviser/cookies.html"


class SearchView(CommonContextMixin, ListView):
    class ErrorState(object):
        def __init__(self, form):
            self._form = form

        @property
        def template_name(self):
            return "search.html"

        def get_queryset(self):
            return []

        def get_context_data(self):
            errorList = []
            for field, error in self._form.errors.items():
                # choose the first field is the error in form-wide
                if field == "__all__":
                    item = {"text": error[0], "href": "#id_postcode"}
                else:
                    item = {"text": error[0], "href": f"#id_{field}"}
                errorList.append(item)

            return {"form": self._form, "data": {}, "errorList": errorList}

    class EnglandOrWalesState(object):
        def __init__(self, form):
            self._form = form
            self._data = form.search()

        @property
        def template_name(self):
            return "results.html"

        def get_queryset(self):
            return self._data.get("results", None)

        def get_context_data(self):
            pages = LaaLaaPaginator(self._data["count"], 10, 3, self._form.current_page)
            current_page = pages.current_page()
            params = {
                "postcode": self._form.cleaned_data["postcode"],
                "name": self._form.cleaned_data["name"],
            }
            categories = self._form.cleaned_data["categories"]

            # create list of tuples which can be passed to urlencode for pagination links
            category_tuples = [("categories", c) for c in categories]

            def item_for(page_num):
                if len(categories) > 0:
                    page_params = {"page": page_num}
                    href = (
                        "/search?"
                        + urllib.parse.urlencode({**page_params, **params})
                        + "&"
                        + urllib.parse.urlencode(category_tuples)
                    )
                else:
                    page_params = {"page": page_num}
                    href = "/search?" + urllib.parse.urlencode({**page_params, **params})

                return {"number": page_num, "current": self._form.current_page == page_num, "href": href}

            pagination = {"items": [item_for(page_num) for page_num in pages.page_range]}

            if current_page.has_previous():
                if len(categories) > 0:
                    page_params = {"page": current_page.previous_page_number()}
                    prev_link = (
                        "/search?"
                        + urllib.parse.urlencode({**page_params, **params})
                        + "&"
                        + urllib.parse.urlencode(category_tuples)
                    )
                else:
                    page_params = {"page": current_page.previous_page_number()}
                    prev_link = "/search?" + urllib.parse.urlencode({**page_params, **params})
                pagination["previous"] = {"href": prev_link}

            if current_page.has_next():
                if len(categories) > 0:
                    page_params = {"page": current_page.next_page_number()}
                    href = (
                        "/search?"
                        + urllib.parse.urlencode({**page_params, **params})
                        + "&"
                        + urllib.parse.urlencode(category_tuples)
                    )
                else:
                    page_params = {"page": current_page.next_page_number()}
                    href = "/search?" + urllib.parse.urlencode({**page_params, **params})
                pagination["next"] = {"href": href}

            return {
                "form": self._form,
                "data": self._data,
                "params": params,
                "FEATURE_FLAG_SURVEY_MONKEY": settings.FEATURE_FLAG_SURVEY_MONKEY,
                "pagination": pagination,
            }

    class OtherJurisdictionState(object):
        REGION_TO_LINK = {
            Region.NI: {
                "link": "https://www.nidirect.gov.uk/articles/legal-aid-schemes",
                "region": "Northern Ireland",
            },
            Region.IOM: {
                "link": "https://www.gov.im/categories/benefits-and-financial-support/legal-aid/",
                "region": "the Isle of Man",
            },
            Region.JERSEY: {
                "link": "https://www.legalaid.je/",
                "region": "Jersey",
            },
            Region.GUERNSEY: {
                "link": "https://www.gov.gg/legalaid",
                "region": "Guernsey",
            },
        }

        def __init__(self, region, postcode):
            self._region = region
            self._postcode = postcode

        def get_queryset(self):
            return []

        @property
        def template_name(self):
            return "other_region.html"

        def get_context_data(self):
            region_data = self.REGION_TO_LINK[self._region]
            return {
                "postcode": self._postcode,
                "link": region_data["link"],
                "region": region_data["region"],
            }

    def get(self, request, *args, **kwargs):
        form = AdviserSearchForm(data=request.GET or None)

        if form.is_valid():
            region = form.region
            if region == Region.ENGLAND_OR_WALES or region == Region.SCOTLAND:
                self.state = self.EnglandOrWalesState(form)
            else:
                self.state = self.OtherJurisdictionState(region, form.cleaned_data["postcode"])
        else:
            self.state = self.ErrorState(form)

        return super().get(self, request, *args, **kwargs)

    def get_template_names(self):
        return ["adviser/" + self.state.template_name]

    def get_queryset(self):
        return self.state.get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(self.state.get_context_data())
        return context
