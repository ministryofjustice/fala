from django.http import Http404
from fala.common.category_manager import CategoryManager
from fala.common.regions import Region
from fala.common.laa_laa_paginator import LaaLaaPaginator
import urllib
from django.conf import settings


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
        if "Invalid page" in self._data.get("error", []):
            raise Http404("Page not found")
        else:
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
                "pagination": pagination if len(pagination["items"]) > 1 else {},
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
        region_data = self.REGION_TO_LINK.get(self._region)

        return {
            "postcode": self._postcode,
            "link": region_data["link"],
            "region": region_data["region"],
        }


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

        return {
            "form": self._form,
            "data": {},
            "errorList": errorList,
        }


class CategorySearchErrorState(object):
    def __init__(
        self,
        form,
        category_display_name,
        category_message,
        category_code,
        sub_category_code,
        search_url,
        category_slug,
    ):
        self._form = form
        self.category_display_name = category_display_name
        self.category_message = category_message
        self.category_code = category_code
        self.sub_category_code = sub_category_code
        self.search_url = search_url
        self.category_slug = category_slug

    @property
    def template_name(self):
        return "category_search.html"

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

        self.category_display_name = CategoryManager.slug_from(self.category_code).replace("-", " ").title()

        if self.category_code == "hlpas":
            self.category_display_name = "Housing Loss Prevention Advice Service"

        return {
            "form": self._form,
            "data": {},
            "errorList": errorList,
            "category_slug": self.category_slug,
            "category_code": self.category_code,
            "sub_category_code": self.sub_category_code,
            "category_display_name": self.category_display_name,
            "category_message": self.category_message,
            "search_url": self.search_url,
        }
